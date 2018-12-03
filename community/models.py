from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# 임시 사용자 정보 테이블
class UserInfo(models.Model):
    id = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE, primary_key=True)
    # email = models.EmailField(blank=False, unique=True, null=False)
    nickname = models.CharField(max_length=10, null=True)
    introduce = models.TextField(null=True)
    profile = models.ImageField(blank=True, upload_to="profile")

    def __str__(self):
        return self.nickname

    def make_dict(self):
        if self.profile.name:
            profile = self.profile.path
        else:
            profile = False

        return {'id': self.id.username, 'email': self.id.email, 'nickname': self.nickname, 'introduce': self.introduce, 'profile': profile}


class Follow(models.Model):
    follower = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='following')


# 게시글 테이블
class Post(models.Model):
    content = models.CharField(max_length=120, null=False)
    poster = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    date = models.DateTimeField('date published', auto_now_add=True)
    game_data = models.OneToOneField('gamedata.Ladder', on_delete=models.CASCADE, null=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


# 댓글 테이블
class Comment(models.Model):
    content = models.CharField(max_length=50, null=False)
    commenter = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
