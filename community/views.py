from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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
        'token': request.session._SessionBase__session_key
    }
    return render(request, 'community/timeline.html', context)


def community(request):
    pass


# 글 삭제
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
    return render(request, 'game/opening.html')


class WritePost(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WritePost, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return JsonResponse({'code': 1, 'msg': '지원하지 않는 방식입니다.'}, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        if request.POST['token'] != request.session._SessionBase__session_key :
            return JsonResponse({'code': 2, 'msg': '잘못된 접근입니다.('+request.POST['token']+'/'+request.session._SessionBase__session_key}, json_dumps_params={'ensure_ascii': False})
        try:
            user_obj = User.objects.get(username=request.POST['id'])
        except User.DoesNotExist:
            return JsonResponse({'code': 3, 'msg': '존재하지 않는 사용자입니다.'}, json_dumps_params={'ensure_ascii': False})

        user, is_new = UserInfo.objects.get_or_create(
            defaults={'nickname': user_obj.username, 'email': '%s@opgg.com' % user_obj.username}, id=user_obj)
        Post.objects.create(content=request.POST['content'], poster=user, date=timezone.now())
        return JsonResponse({'code': 0, 'msg': '성공'}, json_dumps_params={'ensure_ascii': False})


# 글 목록 가져오기
# 받아와야 하는 데이터 : user_id(아이디), item_num(한번에 받아올 포스트 개수), page(가져올 페이지)
# 보내는 데이터 : code(성공(0)유무 코드번호), total_num(전체 게시글 개수), total_page(전체 페이지 개수), now_page(현재 페이지 번호),
#           data:[{post:{id(포스트 고유번호), content(글 내용), date(작성일)}, comment:{content(댓글내용), commenter(댓글작성자), date(작성일)}}]
class GetPost(View):
    def get(self, request):
        return self.make_json(int(request.GET['page']), int(request.GET['item_num']), request.GET['user_id'])

    def post(self, request):
        return self.make_json(int(request.POST['page']), int(request.POST['item_num']), request.POST['user_id'])

    def make_json(self, page, item_num, user_id):
        # 올바르지 않은 사용자 접근 예외처리
        try:
            user_obj = User.objects.get(username=user_id)
            user = UserInfo.objects.get(id=user_obj)
        except User.DoesNotExist:
            return JsonResponse({
                'code': 2,
                'total_num': -1,
                'total_page': -1,
                'now_page': page,
            }, json_dumps_params={'ensure_ascii': False})
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'code': 3,
                'total_num': -1,
                'total_page': -1,
                'now_page': page,
            }, json_dumps_params={'ensure_ascii': False})

        posts = Post.objects.filter(poster=user).order_by('-date')
        total_num = len(posts)
        total_page = total_num//item_num

        if total_num%item_num != 0:
            total_page += 1

        if total_page < page:
            return JsonResponse({
                'code': 1,
                'total_num': total_num,
                'total_page': total_page,
                'now_page': page,
            }, json_dumps_params={'ensure_ascii': False})
        elif total_page == page:
            posts = posts[(page-1)*item_num:]
        else:
            start_num = (page-1)*item_num
            posts = posts[start_num:start_num+item_num]

        data = []
        for post in posts:
            _comments = Comment.objects.filter(post=post).order_by('date')[:5]
            comments = []
            for comment in _comments:
                comments.append({'content': comment.content, 'commenter': comment.commenter.make_dict(), 'date': comment.date})
            data.append({
                'post': {'content': post.content, 'id': post.id, 'data': post.date},
                'comments': comments
            })

        context = {
            'code': 0,
            'total_num': total_num,
            'total_page': total_page,
            'now_page': page,
            'data': data
        }

        return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


# 댓글 목록 가져오기
# 받아와야 하는 데이터 : post_id(글 고유번호), item_num(한번에 받아올 댓글 개수), page(가져올 페이지)
# 보내는 데이터 : code(성공(0)유무 코드번호), total_num(전체 댓글 개수), total_page(전체 페이지 개수), now_page(현재 페이지 번호),
#               data:[{content(댓글내용), commenter(댓글작성자), date(작성일)}]
class GetComment(View):
    def get(self, request):
        return self.make_json(int(request.GET['page']), int(request.GET['item_num']), int(request.GET['post_id']))

    def post(self, request):
        return self.make_json(int(request.POST['page']), int(request.POST['item_num']), int(request.POST['post_id']))

    def make_json(self, page, item_num, post_id):
        # 올바르지 않은 게시글 접근 예외처리
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({
                'code': 2,
                'total_num': -1,
                'total_page': -1,
                'now_page': page,
            }, json_dumps_params={'ensure_ascii': False})

        _comments = Comment.objects.filter(post=post).order_by('date')
        total_num = len(_comments)
        total_page = total_num // item_num

        if total_num % item_num != 0:
            total_page += 1

        if total_page < page:
            return JsonResponse({
                'code': 1,
                'total_num': total_num,
                'total_page': total_page,
                'now_page': page,
            }, json_dumps_params={'ensure_ascii': False})
        elif total_page == page:
            _comments = _comments[(page - 1) * item_num:]
        else:
            start_num = (page - 1) * item_num
            _comments = _comments[start_num:start_num + item_num]

        comments = []
        for comment in _comments:
            comments.append(
                {'content': comment.content, 'commenter': comment.commenter.make_dict(), 'date': comment.date})

        data = list(comments)

        context = {
            'code': 0,
            'total_num': total_num,
            'total_page': total_page,
            'now_page': page,
            'data': data
        }

        return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


# 키워드가 포함된 아이디 혹은 닉네임을 가지는 유저목록검색
# 받아와야하는 데이터 : keyword(검색 키워드)
# 보내는 데이터 : data:[{id(유저 아이디), email(이메일), nickname(닉네임), profile(프로필 사진주소)}]
class GetUserList(View):
    def get(self, request):
        return self.make_json(request.GET['keyword'])

    def post(self, request):
        return self.make_json(request.POST['keyword'])

    def make_json(self, keyword):
        users = User.objects.filter(username__contains=keyword)
        data = []
        for user in users:
            userinfo = UserInfo.objects.get(pk=user)
            data.append(userinfo.make_dict())

        return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii': False})


class AuthLogin(View):
    def get(self, request):
        return JsonResponse({'code': 1, 'msg': '지원하지 않는 방식입니다.'}, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        user = authenticate(request, username=request.POST['id'], password=request.POST['pw'])

        if user is None:
            return JsonResponse({'code': 2, 'msg': '일치하는 계정이 없습니다.'}, json_dumps_params={'ensure_ascii': False})
        else:
            login(request, user)
            return JsonResponse({'code': 0, 'id': user, 'token': request.session._SessionBase__session_key}, json_dumps_params={'ensure_ascii': False})


class Login(View):
    @csrf_exempt
    def get(self, request):
        # er\for Test purpose
        return render(request, 'for_develop/login.html')

    @csrf_exempt
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
