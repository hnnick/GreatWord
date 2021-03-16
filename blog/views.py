from django.shortcuts import render

# Create your views here.
from .models import BlogArticles


def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/titles.html", {"blogs": blogs})


def blog_article(request, article_id):
    article_id = BlogArticles.objects.get(id=article_id)
    pub = article_id.publish
    return render(request, "blog/content.html", {"article": pub})
