
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from .models import Article


def main_page(request):
    articles = Article.objects.filter(
        status=Article.Status.PUBLISHED
    ).order_by("-published_at", "-pk")[:3]

    return render(
        request,
        "pages/home.html",
        {"articles": articles},
    )


def article_list(request):
    articles = Article.objects.filter(
        status=Article.Status.PUBLISHED
    ).order_by("-published_at")

    paginator = Paginator(articles, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "pages/article_list.html",
        {"page_obj": page_obj},
    )


def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        status=Article.Status.PUBLISHED,
    )

    return render(
        request,
        "pages/article_detail.html",
        {"article": article},
    )
