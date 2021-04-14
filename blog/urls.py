

from django.conf.urls import url
from django.urls import include

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.blog_title, name="blog_title"),
    #url(r'( ?P<article_id>\d)$', views.blog_article, name="blog_article"),
    url(r'(?P<article_id>\d)/$', views.blog_article, name="blog_detail"),
    url(r'^article/', include(('article.urls', "article"), namespace='article')),

]
