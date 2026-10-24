from django.test import TestCase
from django.db import IntegrityError, transaction

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