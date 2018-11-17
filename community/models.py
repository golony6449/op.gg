from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# 임시 사용자 정보 테이블
class UserInfo(models.Model):
    id = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE, primary_key=True)
    email = models.EmailField(blank=False, unique=True, null=False)
    nickname = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.nickname


# 게시글 테이블
class Post(models.Model):
    content = models.CharField(max_length=120, null=False)
    poster = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')


# 댓글 테이블
class Comment(models.Model):
    content = models.CharField(max_length=50, null=False)
    commenter = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
