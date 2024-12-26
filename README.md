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

### 회원기능
--------------------------------------------------------
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
--------------------------------------------------------
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
--------------------------------------------------------
# 로그아웃
@require_http_methods(['POST'])
@login_required
def user_logout(request):
    auth_logout(request)
    return redirect('/')

-----------------------------------------------------------------------------------------
