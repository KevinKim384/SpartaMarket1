# 1. 개요
## 1.1 프로젝트 정보
**프로젝트명**: SpartaMarket
간단한 로그인과, 로그인을 통해 글과 여러가지 아이템을 올려, 다른 유저들도 볼 수 있게 해주는 간단한 Django 프레임워크를 이용한 웹입니다.
**개발 기간**: 24.12.24.(목)~24.12.26(월), 3일 간
#프로젝트 일정
| 날짜              | 목표                                                           | 비고  |
|-------------------|--------------------------------------------------------------|-------|
| **12/24(화)**     | 기본  | 1일   |
| **12/25(수)** | - 코드 디버깅 작업, 및 추가                                      | 1일   |
| **12/26(목)**       | - 최종 점검 및 회고<br>- ERD, README 작성                          | 1일   |

개발인원 1명
| 이름(구분)          | 역할 및 기여도                                                                                              |
|---------------------|------------------------------|
| **김준기(개인)**     | - 개인 코드 작성 및 디버깅 처리

# 1.2 프로젝트 목적
Django 기초에 대한 지식을 높이고, 기초적인 문법과 디버깅 해결 능력 향상을 위한 개인 프로젝트

# 2. 주요 기능
### 회원 기능
 - 로그인 / 회원가입 / 로그아웃
### 유저 기능
 - 유저네임, 가입일, 사용자가 등록한 물품 시각적 제공 및 follow 기능(몇명인지 표시)
### 게시 기능
 - 사용자가 적은 게시글을 사용자가 조회하기 / 등록하기 / 수정하기 / 삭제하기 / 찜하기(Like) 기능 포함

대표적인 코드의 흐름(ERD)
ERD
![전체적 ERD](https://github.com/user-attachments/assets/6ea4c78e-e5e3-47a7-b950-6416c5076694)

# 회원기능
--------------------------------------------------------
### 로그인
```
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
--------------------------------------------------------
### 회원가입
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
--------------------------------------------------------
### 로그아웃
@require_http_methods(['POST'])
@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('/')
```

# 2. 유저 기능
```
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
# 팔로우 기능
@login_required
def follow(request, username):
    user = get_object_or_404(Users, username=username)
    if user != request.user:
        if user in request.user.follows.all():
            request.user.follows.remove(user)
        else:
            request.user.follows.add(user)
    return redirect('account:user_detail', username=username)
```
# 게시 기능
```
# 전체 목록 조회
@login_required
def articles(request):
    forms = Article.objects.all().order_by('-created_at')
    user = request.user
    context = {'forms':forms, 'user' : user}
    return render(request, 'article/article.html', context)
#--------------------------------------------------------
# 새로운 게시글 작성
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
# 게시글 저장
@login_required
def save_article(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    new_article = Article.objects.create(title=title, content=content, author = request.user)
    return redirect("article:articles")
#--------------------------------------------------------
# 게시글 자세히 보기기
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
# 게시글 삭제
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
# 게시글 찜하기
@login_required
def article_like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('article:article_detail', article_pk)
```

# 3. 기술 스텍
- 언어: Python 3.10+
- 프레임워크: Django

- Backend:Django
- 저장소: SQLite
- 협업도구: GitHub, Slack, Notion

# 4. 트러블 슈팅
- 1. 모델
     -모델의 N:M, 1:N의 관계가 명확하지 않아 오류 발생
     -확인 후 제대로 된 값을 전달 및 해결
- 2. forms
     -forms에서 fields명을 똑바로 하지 않아 오류 발생
     -확인 후 models에 문제가 있는 것을 발견 및 해결
- 3. views
     -views에서 HTML과 연결이 안되는 오류 발견(특히 id, username 전달 문제)
     -Models에 있는 관계 확인 후 디버깅 실행 및 해결 완료
- 4. HTML
     -TemplateNotFound 등 views와 연결 문제 발생
     -확인 후 fields의 값에 문제 발견. 디버깅 실행 및 해결
# 5. 향후 개선 계획
- 1. 향후 개별 프로필 사진 기능, 각 게시물에 찜수 / 조회수 시각적 표현, 해시태그, 검색 기능 구현
