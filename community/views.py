from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from .models import User, Post, Comment


# 유저 개인 타임라인
def timeline(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(poster=user).order_by('-date')
    data = []
    for post in posts:
        data.append({'post': post, 'comments': Comment.objects.filter(post=post).order_by('date')})
    context = {
        'data_list': data,
        'user': user,
    }
    return render(request, 'community/timeline.html', context)


def community(request):
    pass


# 글 작성
def write_post(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    Post.objects.create(content=request.POST['content'], poster=user, date=timezone.now())
    return HttpResponseRedirect(reverse('community:timeline', args=(user_id,)))


# 댓글 작성
def write_comment(request, post_id):
    user = get_object_or_404(User, pk=request.POST['commenter_id'])
    post = get_object_or_404(Post, pk=post_id)
    Comment.objects.create(content=request.POST['content'], post=post, commenter=user, date=timezone.now())
    return HttpResponseRedirect(reverse('community:timeline', args=(post.poster.id,)))


def read(request):
    pass
