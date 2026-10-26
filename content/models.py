from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT= "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length= 200)
    slug = models.SlugField(max_length=220, unique=True)
    body= models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles"
    )

    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.DRAFT
        ) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    
    class Meta:
        ordering= ["-created_at"]
    
    def save(self, *args, **kwargs):
        if(
            self.status == self.Status.PUBLISHED 
            and self.published_at is None
        ):
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

