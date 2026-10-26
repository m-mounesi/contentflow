
from django.urls import path

from .views import article_detail, article_list, main_page

app_name = "content"

urlpatterns = [
    path("", main_page, name="home"),
    path("articles/", article_list, name="article_list"),
    path("articles/<slug:slug>/", article_detail, name="article_detail"),
]
