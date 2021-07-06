from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ArticleColumn, ArticlePost, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import redis
from django.conf import settings
from .forms import CommentForm

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        article_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        article_title = ArticlePost.objects.all()

    paginator = Paginator(article_title, 2)
    page = request.GET.get("page")
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request, "article/list/author_articles.html", {"articles": articles, "page": current_page})
    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page})


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    # total_views：记录文章访问量
    # 一般通过“对象类型：对象ID：对象属性”来命名一个键
    total_view = r.incr("article:{}:views".format(article.id))
    print(total_view)
    # zincrby的原型是zincrby(name,amount,value):根据amount所设定的步长值增加有序集合（name）中的value的数值
    # 实现了article_ranking中的article.id以步长1自增，
    # 即文章访问一次，article_ranking就将文章id的值增1
    r.zincrby('article_ranking', 1, article.id)
    # 得到article_ranking中排序前10名对象
    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    print(article_ranking)
    # 得到前10名文章ID
    article_ranking_ids = [int(id) for id in article_ranking]
    print(article_ranking_ids)
    # 查询出id在article_ranking_ids这个范围内的所有文章对象，并以文章对象为元素生成列表
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    print(most_viewed)
    # 对所得到的列表进行排序
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
    print("---------")
    print(most_viewed)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    article_tags_ids = article.article_tag.values_list("id", flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count("article_tag")).order_by('-same_tags', '-created')[:4]
    print("++++++")
    print(similar_articles)
    return render(request, "article/list/article_detail.html",
                  {"article": article, "total_views": total_view,
                   "most_viewed": most_viewed, "comment_form": comment_form,
                   "similar_articles": similar_articles})


@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
               article.users_like.add(request.user)
               return HttpResponse("1")
            else:
               article.users_like.remove(request.user)
               return HttpResponse("2")
        except:
            return HttpResponse("no")
