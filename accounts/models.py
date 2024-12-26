from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

def user_profile_image_path(instance, filename):
    return f'profile_images/{instance.username}/{filename}'

class Users(AbstractUser):
    username = models.CharField(max_length=50, unique= True)
    password = models.CharField(max_length=50, unique= True)
    created_at= models.DateTimeField("생성 날짜", auto_now_add = True) 
    updated_at = models.DateTimeField("수정 날짜", auto_now = True)
    #follows - user모델이 특정 유저가 펄로우 한 user id 목록을 얻고싶을 때 쓰는 필드
    #followers - user모델이 특정 유저를 펄로우 한 user id 목록을 얻고 싶을 때 쓰는 필드
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank = True)

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.follows.count()
    
    def __str__(self):
        return self.username