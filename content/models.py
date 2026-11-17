from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    body = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")

        # A partial save that does not include either field must not change
        # publication metadata based on unsaved in-memory status changes.
        should_sync_publication = (
            update_fields is None
            or "status" in update_fields
            or "published_at" in update_fields
        )

        if should_sync_publication:
            previous_published_at = self.published_at

            if self.status == self.Status.PUBLISHED:
                if self.published_at is None:
                    self.published_at = timezone.now()
            else:
                self.published_at = None

            if (
                update_fields is not None
                and self.published_at != previous_published_at
            ):
                kwargs["update_fields"] = set(update_fields) | {"published_at"}

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
