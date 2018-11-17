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
from . import views

app_name = 'community'
urlpatterns = [
    path('<str:post_id>/write_comment', views.write_comment, name='write_comment'),
    path('<str:user_id>/write_post', views.write_post, name='write_post'),
    path('<str:user_id>/', views.timeline, name='timeline'),
    # path('/send_game_data', send_game_data, 'send_game_data'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
]
