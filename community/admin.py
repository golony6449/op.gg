from django.contrib import admin

from .models import UserInfo, Post, Comment, GamePost

admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(GamePost)
