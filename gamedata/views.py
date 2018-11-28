from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gamedata.models import *
import json

from .module.key_generator import KeyGenerator
from .module.check_sync_data import *


def register_game_data(request):

    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return HttpResponse('Not authorized', status=400)

    generator = KeyGenerator()
    # income = json.dump(request.body)

    new_gamedata = Gamedata()
    # new_gamedata.game_name = income['game_name']
    # new_gamedata.score_type = income['score_type']
    new_gamedata.game_name = request.GET['game_name']
    new_gamedata.score_type = request.GET['score_type']
    new_gamedata.api_key = generator.key_gen()

    try:
        # user_obj = User.objects.find(income['id'])
        user_obj = User.objects.find(request.GET['id'])
    except User.DoesNotExist:
        # return HttpResponse('Incorrect ID', status=400)
        return JsonResponse({'code': 400, 'msg':'Incorrect ID'}, status=400)

    new_gamedata.admin_name = user_obj

    # return HttpResponse('Successfully registered')
    return JsonResponse({'code': 200, 'msg': 'Successfully register'})


# For development
class RegisterTemp(View):
    def get(self, request):
        return render(request, 'for_develop/reg_game_temp.html')

    def post(self, request):
        generator = KeyGenerator()

        new_gamedata = Gamedata()
        new_gamedata.game_name = request.POST['game_name']
        new_gamedata.score_type = request.POST['score_type']
        new_gamedata.api_key = generator.key_gen()
        new_gamedata.admin_name = request.user

        new_gamedata.save()

        return redirect(test)

@csrf_exempt
def sync(request):
    # income = json.dumps(request.body)

    # 예외처리
    if check_sync_data(request.GET) is False:
        return JsonResponse({'code': 400, 'message': 'Wrong or Missing key'}, status=400)

    new_ladder_data = Ladder()
    # new_ladder_data.game_index = Gamedata.objects.find(income['api_key'])
    # new_ladder_data.score = income['score']
    new_ladder_data.game_index = Gamedata.objects.find(request.GET['api_key'])
    new_ladder_data.score = request.GET['score']

    try:
        # user_obj = User.objects.get(username=income['player_id'])
        user_obj = User.objects.get(username=request.GET['player_id'])
    except User.DoesNotExist:
        return JsonResponse({'code': 400, 'message': 'Wrong User name'}, status=400)
    new_ladder_data.player_id = user_obj

    new_ladder_data.save()

    return JsonResponse({'code': 200, 'message': 'Successfully synced'})


def test(request):
    all = Ladder.objects.all()
    all_game_data = Gamedata.objects.all()

    return render(request, 'gamedata/test.html', {'all_data': all, 'all_game_data': all_game_data})


def request_ladder_data(request):
    # income = json.dumps(request.body)

    # ladder_info_list = Ladder.objects.filter(player_id=income['player_id'])[:10]
    ladder_info_list = Ladder.objects.filter(player_id=request.GET['player_id'])[:10]
    result = dict()
    for index, info in enumerate(ladder_info_list):
        result[index] = {'code': 200, 'game_title': info.game_index.game_name, 'score': info.score}

    return JsonResponse(result)
