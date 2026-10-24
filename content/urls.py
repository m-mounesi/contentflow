
from django.urls import path
from .views import article_list, article_detail


app_name = "content"


urlpatterns = [
    path("", article_list, name="article_list"),
    path(
        "articles/<slug:slug>/",
        article_detail,
        name="article_detail",
    ),
]
