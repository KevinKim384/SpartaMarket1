from django.urls import path, include
from .import views

app_name = 'account'
urlpatterns = [
    path('', views.signin, name = 'signin'),
    path('signup/', views.signup, name = 'signup'),
    path('account_detail/<str:username>/', views.account_detail, name = 'account_detail'),
    path('user_detail/<str:username>/', views.user_detail, name = 'user_detail'),
    #--------------------------------------------------------------------------
    path('user_logout/', views.user_logout, name = 'user_logout'),
    path('out_membership/', views.out_membership, name = 'out_membership'),
    path('user_delete/', views.user_delete, name = 'user_delete'),
    path('follow/<str:username>/', views.follow, name='follow'),
]