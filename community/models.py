from django.db import models


# 임시 사용자 정보 테이블
class User(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    email = models.EmailField(blank=False, unique=True, null=False)
    password = models.CharField(max_length=15, null=False)
    nickname = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.nickname


# 게시글 테이블
class Post(models.Model):
    content = models.CharField(max_length=120, null=False)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')


# 댓글 테이블
class Comment(models.Model):
    content = models.CharField(max_length=50, null=False)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
