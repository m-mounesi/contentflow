from django.contrib import admin

from .models import Article, Category



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ("name", "slug", "created_at")
    search_fields= ("name",)
    prepopulated_fields= {"slug": ("name",)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "status",
        "created_at",
        "published_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "category",
        "created_at",
        "published_at",
    )

    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    list_per_page = 20