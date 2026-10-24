from django.test import TestCase
from django.db import IntegrityError, transaction

from django.urls import reverse

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

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
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

    def test_article_list_shows_published_articles(self):
        response = self.client.get(
            reverse("content:article_list")
        )

        self.assertEqual(response.status_code, 200)
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


