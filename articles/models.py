from django.db import models
from accounts.models import Users
from django.conf import settings

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at= models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #likes - article 모델이 해당 게시글을 좋아요 한 user id 목록을 얻고싶을 때 쓰는 필드
    #liked_product - user모델이 특정 유저가 좋아요 한 게시글의 id 목록을 얻고 싶을 때 쓰는 필드
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = False, related_name='articles')
    
    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title