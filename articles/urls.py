from django.urls import path, include
from .import views
app_name = 'article'
urlpatterns = [
    path('articles/', views.articles, name = 'articles'),
    path('new_article/', views.new_article, name = 'new_article'),
    path('save_article/', views.save_article, name = 'save_article'),
    path('article_detail/<int:article_pk>/', views.article_detail, name = 'article_detail'),
    path("article_detail/<int:article_pk>/delete/", views.delete_article, name="delete_article"),
    path("article_detail/<int:article_pk>/delete/delete_complete/", views.delete_complete, name = 'delete_complete'),
    path('<int:article_pk>/like/', views.article_like, name='article_like'),
]
