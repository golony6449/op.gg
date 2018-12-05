from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View

from .models import UserInfo, Post, Comment, Follow, GamePost
from gamedata.models import Gamedata, Ladder


# 유저 개인 타임라인
def timeline(request, user_id):
    try:
        user_obj = User.objects.get(username=user_id)
    except User.DoesNotExist:
        return HttpResponse('존재하지 않는 사용자 입니다.', status=400)

    user = UserInfo.objects.get(id=user_obj)
    # posts = Post.objects.filter(poster=user).order_by('-date')
    # data = []
    # for post in posts:
    #     data.append({'post': post, 'comments': Comment.objects.filter(post=post).order_by('date')})

    following = len(Follow.objects.filter(follower=user))
    follower = Follow.objects.filter(following=user)

    game_list = []

    if request.user.is_authenticated:
        try:
            login_user = UserInfo.objects.get(id=request.user)
            game_list = Gamedata.objects.filter(admin_name=request.user)
            if len(follower.filter(follower=login_user)) == 1:
                followed = True
            else:
                followed = False
        except User.DoesNotExist:
            followed = False
    else:
        followed = False

    follower = len(follower)

    # 동일 유저 여부 확인
    if request.user == user_obj:
        admin_mode = True
    else:
        admin_mode = False

    ladder_info_list = Ladder.objects.filter(player_id=request.user).order_by('-index')[:10]

    context = {
        # 'data_list': data,
        'page_user': user,
        'following': following,
        'follower': follower,
        'followed': followed,
        'title': user_id + '\'s Timeline',
        'game_list': game_list,
        'admin_mode': admin_mode,
        'mode': 'user_profile',
        'ladder_list': ladder_info_list
    }
    return render(request, 'timeline.html', context)


def toggle_follow(request):
    if request.user:
        try:
            user = User.objects.get(username=request.GET['id'])
            page_user = UserInfo.objects.get(id=user)
            user = User.objects.get(username=request.user.username)
            login_user = UserInfo.objects.get(id=user)
        except User.DoesNotExist:
            return JsonResponse({
                'code': 0
            }, json_dumps_params={'ensure_ascii': False})
        except UserInfo.DoesNotExist:
            return JsonResponse({
                'code': 0
            }, json_dumps_params={'ensure_ascii': False})

        try:
            follow = Follow.objects.get(following=page_user, follower=login_user)
            Follow.delete(follow)
            following = len(Follow.objects.filter(follower=page_user))
            follower = len(Follow.objects.filter(following=page_user))
            return JsonResponse({
                'code': 0,
                'following': following,
                'follower': follower
            }, json_dumps_params={'ensure_ascii': False})
        except Follow.DoesNotExist:
            follow = Follow.objects.create(following=page_user, follower=login_user)
            follow.save()
            following = len(Follow.objects.filter(follower=page_user))
            follower = len(Follow.objects.filter(following=page_user))
            return JsonResponse({
                'code': 1,
                'following': following,
                'follower': follower
            }, json_dumps_params={'ensure_ascii': False})


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


def check_id(request):
    try:
        User.objects.get(username=request.GET['id'])
        return JsonResponse({
            'code': 0
        }, json_dumps_params={'ensure_ascii': False})
    except User.DoesNotExist:
        return JsonResponse({
            'code': 1
        }, json_dumps_params={'ensure_ascii': False})


def read(request):
    pass


def game(request):
    return render(request, 'game/opening.html')


class WritePost(View):
    def get(self, request):
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            try:
                user = UserInfo.objects.get(id=request.user)
            except UserInfo.DoesNotExist:
                return redirect('timeline', request.user.username)
            Post.objects.create(content=request.POST['content'], poster=user, date=timezone.now())
            return redirect('timeline', request.user.username)
        return redirect('login')


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
            posts = posts[(page - 1) * item_num:]
        else:
            start_num = (page - 1) * item_num
            posts = posts[start_num:start_num + item_num]

        data = []
        for post in posts:
            if post.game_data:
                is_game_data = True
                game_data = {'name': post.game_data.game_index.game_name, 'img': post.game_data.game_index.image.url,
                             'score': post.game_data.score}
            else:
                is_game_data = False
                game_data = False
            data.append({
                'post': {'content': post.content, 'id': post.id, 'date': post.date, 'is_game': is_game_data},
                'game_data': game_data
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


class SignUp(View):
    def get(self, request):
        return render(request, 'Auth/Auth.html')

    def post(self, request):
        user = User.objects.create_user(request.POST['id'], request.POST['email'], request.POST['pw'])
        user.save()
        UserInfo.objects.create(id=user, nickname=request.POST['nickname'], profile=request.FILES['img'],
                                mode=request.POST['is_dev'], introduce=request.POST['introduce'])

        return render(request, 'Auth/Auth.html')


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('timeline', request.user.username)
        return render(request, 'Auth/Auth.html')

    def post(self, request):
        user = authenticate(request, username=request.POST['id'], password=request.POST['pw'])

        if user is None:
            return render(request, 'Auth/Auth.html')
        else:
            login(request, user)
            return redirect('timeline', user.username)


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return redirect('login')


def search(request):
    params = dict()
    params['keyword'] = request.GET['keyword']

    # TODO: 검색기능 구현

    # 게임 목록
    game_list = Gamedata.objects.filter(game_name__contains=request.GET['keyword'])
    params['game_list'] = game_list

    # 유저 검색
    user_list = User.objects.filter(username__contains=request.GET['keyword'])
    params['user_list'] = user_list

    user_info_list = list()

    for user in user_list:
        user_info_list.append(UserInfo.objects.get(id=user))
    params['user_info_list'] = user_info_list

    return render(request, 'Search.html', params)


def game_profile(request, game_name):
    params = dict()
    params['title'] = 'Game Profile'
    params['mode'] = 'game_profile'

    # 요청 받은 페이지의 게임 정보 확인
    try:
        game_data = Gamedata.objects.get(game_name=game_name)
        params['game_data'] = game_data
        params['page_user'] = game_data.admin_name
    except Gamedata.DoesNotExist:
        return HttpResponse('해당하는 게임이름이 없습니다.')

    # 게임에 대한 공지사항
    notice_list = GamePost.objects.filter(game_data=game_data).order_by('-date')
    params['notice_list'] = notice_list

    # 순위 상위 10개 추출
    ladder_list = Ladder.objects.filter(game_index=game_data).order_by('-score')[:10]
    params['ladder_list'] = ladder_list

    params['game_list'] = Gamedata.objects.filter(admin_name=request.user)

    # 동일 유저 여부 확인
    if request.user == game_data.admin_name:
        params['admin_mode'] = True
    else:
        params['admin_mode'] = False

    return render(request, 'timeline_game.html', params)


class WriteGamePost(View):
    def get(self, request):
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            try:
                game_data = Gamedata.objects.get(game_name=request.POST['game_name'])
            except Gamedata.DoesNotExist:
                return HttpResponse('올바르지 않은 접근 입니다. (잘못된 게임 명)')

            GamePost.objects.create(content=request.POST['content'], game_data=game_data, date=timezone.now())
            return redirect('game', game_name=request.POST['game_name'])
        return redirect('login')
