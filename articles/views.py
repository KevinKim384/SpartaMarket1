from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout 
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import ArticleForm, NewArticleForm
from .models import Article
from accounts.models import Users
# Create your views here.

@login_required
def articles(request):
    forms = Article.objects.all().order_by('-created_at')
    user = request.user
    context = {'forms':forms, 'user' : user}
    return render(request, 'article/article.html', context)
#--------------------------------------------------------
@require_http_methods(['GET', 'POST'])
@login_required
def new_article(request):
    if request.method == 'POST':
        form = NewArticleForm(request.POST)
        if form.is_valid():
            form.save(commit = False)
            form.author = request.user
            form.save()
            return redirect('article:articles')
    else:
        form = NewArticleForm()
        context = {
            'form' : form
        }
    return render(request, 'article/new_article.html', context)
#--------------------------------------------------------
@login_required
def save_article(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    new_article = Article.objects.create(title=title, content=content, author = request.user)
    return redirect("article:articles")
#--------------------------------------------------------
@require_http_methods(['GET', 'POST'])
@login_required
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance = article)
        if form.is_valid():
            form.save()
            return redirect('article:articles')
    else:
        form = ArticleForm(instance = article)
        context = {
            'form':form,
            'article':article
        }
        return render(request, 'article/article_detail.html', context)
#--------------------------------------------------------
@login_required
def delete_article(request, article_pk):
    del_article = Article.objects.get(pk=article_pk)
    context = {'del_article' : del_article}
    return render(request, 'article/delete_article.html', context)

@require_http_methods(['POST'])
@login_required
def delete_complete(request, article_pk):
    product = Article.objects.get(pk=article_pk)
    product.delete()
    return redirect("article:articles")
#--------------------------------------------------------
@login_required
def article_like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('article:article_detail', article_pk)
#--------------------------------------------------------