from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views import View
from .models import UserInfo, Post, Comment


# 유저 개인 타임라인
def timeline(request, user_id):
    try:
        user_obj = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponse('존재하지 않는 사용자 입니다.', status=400)

    user = get_object_or_404(UserInfo, pk=user_obj)
    posts = Post.objects.filter(poster=user).order_by('-date')
    data = []
    for post in posts:
        data.append({'post': post, 'comments': Comment.objects.filter(post=post).order_by('date')})
    context = {
        'data_list': data,
        'page_user': user,
    }
    return render(request, 'community/timeline.html', context)


def community(request):
    pass


# 글 작성
def write_post(request, user_id):
    try:
        user_obj = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponse('존재하지 않는 사용자 입니다.', status=400)

    user = get_object_or_404(UserInfo, pk=user_obj)
    Post.objects.create(content=request.POST['content'], poster=user, date=timezone.now())
    return HttpResponseRedirect(reverse('timeline', args=(user_id,)))


# 댓글 작성
def write_comment(request, post_id):
    try:
        user_obj = User.objects.get(username=request.POST['commenter_id'])
    except User.DoesNotExist:
        return HttpResponse('존재하지 않는 사용자 입니다.', status=400)

    user = get_object_or_404(UserInfo, pk=user_obj)
    post = get_object_or_404(Post, pk=post_id)
    Comment.objects.create(content=request.POST['content'], post=post, commenter=user, date=timezone.now())
    return HttpResponseRedirect(reverse('timeline', args=(post.poster.id,)))


def read(request):
    pass


class Login(View):
    def get(self, request):
        # er\for Test purpose
        return render(request, 'for_develop/login.html')

    def post(self, request):
        user = authenticate(request, username=request.POST['id'], password=request.POST['pw'])

        if user is None:
            return HttpResponse('Fail')
        else:
            login(request, user)
            return HttpResponse('Success')


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return redirect('login')
