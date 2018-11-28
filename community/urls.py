"""opgg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from community.views import Login, Logout, GetPost, GetComment, GetUserList, AuthLogin, WritePost
from . import views

# app_name = 'community'
urlpatterns = [
    path('<int:post_id>/write_comment', views.write_comment, name='write_comment'),
    path('<int:post_id>/delete_post', views.delete_post, name='delete_post'),
    # path('/send_game_data', send_game_data, 'send_game_data'),
    path('rest/getPost', GetPost.as_view(), name='getPost'),
    path('rest/getComment', GetComment.as_view(), name='getComment'),
    path('rest/getUserList', GetUserList.as_view(), name='getUserList'),
    path('rest/writePost', WritePost.as_view(), name='writePost'),
    path('rest/auth/login', AuthLogin.as_view(), name='authLogin'),
    path('rest/auth/logout', Logout.as_view(), name='authLogout'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('<str:user_id>', views.timeline, name='timeline'),
    # path('game', game, name='game'),
]
