from datetime import timedelta

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.dateformat import format as date_format

from .models import Article, Category


class CategoryModelTests(TestCase):
    def test_category_str_returns_name(self):
        category= Category.objects.create(
            name = "Technology",
            slug= "technology"
        )

        self.assertEqual(str(category), "Technology")


class ArticleModelsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )

    def test_article_str_returns_title(self):
        article = Article.objects.create(
            title="Django Basics",
            slug="django-basics",
            body="Introduction to Django.",
            category=self.category,
        )

        self.assertEqual(str(article), "Django Basics")

    def test_article_defaults_to_draft(self):
        article= Article.objects.create(
            title="New Article",
            slug="new-article",
            body="Article content.",
            category=self.category,
        )

        self.assertEqual(article.status, Article.Status.DRAFT)

    def test_article_slug_must_be_unique(self):
        Article.objects.create(
            title="First Article",
            slug="same-slug",
            body="First body.",
            category=self.category,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            Article.objects.create(
                title="Second Article",
                slug="same-slug",
                body="Second body.",
                category=self.category,
            )

    def test_publishing_article_sets_published_at(self):
        article = Article.objects.create(
            title="Publish Me",
            slug="publish-me",
            body="Content",
            category=self.category,
        )

        self.assertIsNone(article.published_at)

        article.status = Article.Status.PUBLISHED
        article.save()

        self.assertIsNotNone(article.published_at)


    def test_editing_published_article_preserves_published_at(self):
        article = Article.objects.create(
            title="Published Article",
            slug="published-article",
            body="Content",
            category=self.category,
            status=Article.Status.PUBLISHED,
        )

        original_published_at = article.published_at

        article.title = "Updated Title"
        article.save()

        self.assertEqual(
            article.published_at,
            original_published_at,
        )




class ArticleViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )

        self.published_article = Article.objects.create(
            title="Django Basics",
            slug="django-basics",
            body="Introduction to Django.",
            category=self.category,
            status=Article.Status.PUBLISHED,
        )

        self.draft_article = Article.objects.create(
            title="Draft Article",
            slug="draft-article",
            body="This is a draft.",
            category=self.category,
            status=Article.Status.DRAFT,
        )

    def test_home_shows_three_most_recent_published_articles(self):
        now = timezone.now()
        self.published_article.published_at = now - timedelta(days=2)
        self.published_article.save(update_fields=["published_at"])

        older_article = Article.objects.create(
            title="Older Article",
            slug="older-article",
            body="Older published content.",
            category=self.category,
            status=Article.Status.PUBLISHED,
            published_at=now - timedelta(days=3),
        )
        second_article = Article.objects.create(
            title="Second Article",
            slug="second-article",
            body="Second published content.",
            category=self.category,
            status=Article.Status.PUBLISHED,
            published_at=now - timedelta(days=1),
        )
        newest_article = Article.objects.create(
            title="Newest Article",
            slug="newest-article",
            body="Newest published content.",
            category=self.category,
            status=Article.Status.PUBLISHED,
            published_at=now - timedelta(hours=1),
        )

        response = self.client.get(reverse("content:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse("content:home"), "/")
        self.assertEqual(
            [article.title for article in response.context["articles"]],
            ["Newest Article", "Second Article", "Django Basics"],
        )
        self.assertContains(response, self.category.name)
        self.assertContains(
            response,
            date_format(newest_article.published_at, "M j, Y"),
        )
        for article in (newest_article, second_article, self.published_article):
            self.assertContains(response, article.title)
            self.assertContains(
                response,
                reverse("content:article_detail", kwargs={"slug": article.slug}),
            )
        self.assertNotContains(response, older_article.title)
        self.assertNotContains(response, self.draft_article.title)

    def test_home_shows_empty_state_when_no_articles_are_published(self):
        Article.objects.all().delete()

        response = self.client.get(reverse("content:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "هنوز هیچ مقاله‌ای منتشر نشده است.")
        self.assertEqual(list(response.context["articles"]), [])

    def test_home_shows_categories(self):
        Category.objects.create(name="Python", slug="python")
        Category.objects.create(name="Design", slug="design")

        response = self.client.get(reverse("content:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "Design")
        self.assertContains(response, "دسته‌بندی‌ها")

    def test_home_shows_empty_categories_state(self):
        Article.objects.all().delete()
        Category.objects.all().delete()

        response = self.client.get(reverse("content:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "هنوز دسته‌بندی‌ای اضافه نشده است.")

    def test_article_list_shows_published_articles(self):
        response = self.client.get(
            reverse("content:article_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse("content:article_list"), "/articles/")
        self.assertTemplateUsed(response, "pages/article_list.html")
        self.assertContains(response, "Django Basics")
        self.assertNotContains(response, "Draft Article")

    def test_article_list_pagination(self):
        Article.objects.all().delete()
        
        Article.objects.bulk_create([
            Article(
                title=f"Article {i}",
                slug=f"article-{i}",
                body="Test body",
                category=self.category,
                status=Article.Status.PUBLISHED,
            )
            for i in range(12)
        ])

        response = self.client.get(
            reverse("content:article_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 10)
        self.assertTrue(response.context["page_obj"].has_next())

        response = self.client.get(
            reverse("content:article_list"),
            {"page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"]), 2)
        self.assertFalse(response.context["page_obj"].has_next())

    def test_article_detail_shows_published_article(self):
        response = self.client.get(
            reverse(
                "content:article_detail",
                kwargs={"slug": "django-basics"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Basics")
        self.assertContains(response, "Introduction to Django.")

    def test_draft_article_detail_returns_404(self):
        response = self.client.get(
            reverse(
                "content:article_detail",
                kwargs={"slug": "draft-article"},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_missing_article_returns_404(self):
        response = self.client.get(
            reverse(
                "content:article_detail",
                kwargs={"slug": "does-not-exist"},
            )
        )

        self.assertEqual(response.status_code, 404)
