from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/article_column.html", {"columns": columns, "column_form": column_form})
    if request.method == "POST":
        column_name = request.POST["column"]
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        print(article_post_form)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST["column_id"])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm
        article_columns = request.user.article_column.all()
        return render(request, "article/article_post.html",
                      {"article_post_form": article_post_form, "article_columns": article_columns})


@login_required(login_url="/account/login")
def article_list(request):
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list, 2)#根据所查询到的文章对象articles_list创建分页的实例对象，并且规定每页最多2个。
    page = request.GET.get("page")#获得当前浏览器GET请求的参数page的值，也就是当前浏览器所请求的页码数值。
    try:
       current_page = paginator.page(page)#page()时候Paginator对象的一个方法，其作用在于得到指定页面内容，其参数必须大于或等于1的整数
       articles = current_page.object_list#page()是Paginator对象的属性，能够得到该页面所有的对象列表。类似的属性还有Page.number(返回页码)等
    except PageNotAnInteger:#捕获请求页码数值不是整数的异常
       current_page = paginator.page(1)
       articles = current_page.object_list
    except EmptyPage:#捕获请求的野马为空或者URL参数中没有page的异常
       current_page = paginator.page(paginator.num_pages)#paginator.num_pages返回的是页数，num_pages是Paginator的一个属性
       articles = current_page.object_list
    return render(request, "article/article_list.html", {"articles": articles, "page": current_page})


@login_required(login_url="/account/login")
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/article_detail.html", {"article": article})


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title": article.title})
        this_article_column = article.column
        return render(request, "article/redit_article.html", {"article": article, "article_columns": article_columns,
                                                              "this_article_column": this_article_column,
                                                              "this_article_form": this_article_form})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST["column_id"])
            redit_article.title = request.POST["title"]
            redit_article.body = request.POST["body"]
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")


