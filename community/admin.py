from django.contrib import admin

from .models import UserInfo, Post, Comment, GamePost, Follow

admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(GamePost)
admin.site.register(Follow)
