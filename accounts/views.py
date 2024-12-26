from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout 
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, CustomUserUpdateForm, CustomUserPasswordUpdateForm, UserProfileForm, CustomUserUpdateForm2
from .models import Users
from articles.models import Article

#--------------------------------------------------------
# 로그인
@require_http_methods(['GET', 'POST'])
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('article:articles')
        else:
            # 폼이 유효하지 않으면 다시 로그인 폼을 보여주고 에러 메시지를 전달
            return render(request, 'account/signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        context = {
            'form' : form
        }
        return render(request, 'account/signin.html', context)
#--------------------------------------------------------
# 회원가입
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context = {'form': form}
            return render(request, 'account/signin.html', context)
    else:
        form = CustomUserCreationForm(request.POST)
        context = {
            'form' : form
        }
        return render(request, 'account/signup.html', context)
#--------------------------------------------------------
# 계정 자세히 보기
@require_http_methods(['GET', 'POST'])
@login_required
def account_detail(request, username):
    user = get_object_or_404(Users, username=username)
    if request.method == 'POST':
        form1 = CustomUserUpdateForm(request.POST, instance=request.user) 
        form2 =  CustomUserPasswordUpdateForm(request.user, request.POST)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            update_session_auth_hash(request, form2.user)
            auth_logout(request)
            return redirect('/')
        context = {'form1': form1, 'form2': form2, 'user': user}
        return render(request, 'account/account_detail.html', context)
    else:
        form1 = CustomUserUpdateForm2(instance=request.user)
        form2 =  CustomUserPasswordUpdateForm(request.user)
        context = {'form1': form1, 'form2' : form2, 'user' : user}
        return render(request, 'account/account_detail.html', context)
#--------------------------------------------------------
# 유저 자세히 보기
@require_http_methods(['GET', 'POST'])
@login_required
def user_detail(request, username):
    user = get_object_or_404(Users, username=username)
    my_article = Article.objects.filter(author=user)
    liked_articles = user.liked_articles.all()
    follow = request.user.follows.filter(pk=user.pk)
    if request.user.username != username:
        return render(request, 'account/user_detail.html', {'user': user, 'follow' : follow})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:user_detail', username=username)
    else:
        form = UserProfileForm(instance=user)
        context = {
            'form': form,
            'user': user,
            'follow' : follow,
            'my_article': my_article,
            'liked_articles': liked_articles
        }
        return render(request, 'account/user_detail.html', context)
#--------------------------------------------------------
# 로그아웃
@require_http_methods(['POST'])
@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('/')
#--------------------------------------------------------
# 회원탈퇴 페이지 이동
def out_membership(request):
    return render(request, 'account/out_membership.html')
# 회원 삭제
def user_delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect("/")
#--------------------------------------------------------
@login_required
def follow(request, username):
    user = get_object_or_404(Users, username=username)
    if user != request.user:
        if user in request.user.follows.all():
            request.user.follows.remove(user)
        else:
            request.user.follows.add(user)
    return redirect('account:user_detail', username=username)