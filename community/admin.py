from django.contrib import admin

from .models import UserInfo, Post, Comment

admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(Comment)
