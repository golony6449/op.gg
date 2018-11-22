from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views import View
from django.core import serializers
from .models import UserInfo, Post, Comment


# 유저 개인 타임라인
def timeline(request, user_id):
    try:
        user_obj = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponse('존재하지 않는 사용자 입니다.', status=400)

    user, is_new = UserInfo.objects.get_or_create(defaults={'nickname': user_id, 'email': '%s@opgg.com' % user_id}, id=user_obj)
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


# 글 작성
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_id = post.poster.id.username
    post.delete()
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


def game(request):
    return render(request, 'game/start.html')


# jsonResponse 반환
def make_json(data):
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


# 글 목록 가져오기
# 받아와야 하는 데이터 : user_id(아이디), item_num(한번에 받아올 포스트 개수), page(가져올 페이지)
# 보내는 데이터 : code(성공(0)유무 코드번호), total_num(전체 게시글 개수), total_page(전체 페이지 개수), now_page(현재 페이지 번호),
#           data:[{post:{id(포스트 고유번호), content(글 내용), date(작성일)}, comment:{content(댓글내용), commenter(댓글작성자), date(작성일)}}]
class GetPost(View):
    def get(self, request):
        page = int(request.GET['page'])
        item_num = int(request.GET['item_num'])
        user_obj = User.objects.get(username=request.GET['user_id'])
        user = UserInfo.objects.get(id=user_obj)
        posts = Post.objects.filter(poster=user).order_by('-date')
        total_num = len(posts)
        total_page = total_num//item_num

        if total_num%item_num != 0:
            total_page += 1

        if total_page < page:
            return make_json({
                'code': 1,
                'total_num': total_num,
                'total_page': total_page,
                'now_page': page,
            })
        elif total_page == page:
            posts = posts[(page-1)*item_num:]
        else:
            start_num = (page-1)*item_num
            posts = posts[start_num:start_num+item_num]

        data = []
        for post in posts:
            data.append({
                'post': {'content': post.content, 'id': post.id, 'data': post.date},
                'comments': list(Comment.objects.filter(post=post).order_by('date').values('content', 'commenter', 'date')[:5])
            })

        context = {
            'code': 0,
            'total_num': total_num,
            'total_page': total_page,
            'now_page': page,
            'data': data
        }

        return make_json(context)

    def post(self, request):
        pass


class GetComment(View):
    def get(self, request):
        page = int(request.GET['page'])
        item_num = int(request.GET['item_num'])
        post_id = int(request.GET['post_id'])
        post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post=post).order_by('date').values('content', 'commenter', 'date')
        total_num = len(comments)
        total_page = total_num//item_num

        if total_num%item_num != 0:
            total_page += 1

        if total_page < page:
            return make_json({
                'code': 1,
                'total_num': total_num,
                'total_page': total_page,
                'now_page': page,
            })
        elif total_page == page:
            comments = comments[(page-1)*item_num:]
        else:
            start_num = (page-1)*item_num
            comments = comments[start_num:start_num+item_num]

        data = list(comments)

        context = {
            'code': 0,
            'total_num': total_num,
            'total_page': total_page,
            'now_page': page,
            'data': data
        }

        return make_json(context)

    def post(self, request):
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
