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
from .views import *

# /gatedata/
urlpatterns = [
    path('register', register_game_data, name='reg_game_data'),
    path('sync', sync, name='sync'),
    path('request', request_ladder_data, name='request_ladder_data'),
    path('test', test, name='test'),

    # for development
    path('reg_page_temp', RegisterTemp.as_view(), name='reg_page_temp'),    # 개발용 페이지
]
