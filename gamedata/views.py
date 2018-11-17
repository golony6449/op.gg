from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from gamedata.models import *
import json

from .module.key_generator import KeyGenerator
from .module.check_sync_data import *


def register_game_data(request):

    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return HttpResponse('Not authorized', status=400)

    generator = KeyGenerator()
    income = json.dump(request.body)

    new_gamedata = Gamedata()
    new_gamedata.game_name = income['game_name']
    new_gamedata.score_type = income['score_type']
    new_gamedata.api_key = generator.key_gen()

    try:
        user_obj = User.objects.find(income['id'])
    except User.DoesNotExist:
        return HttpResponse('Incorrect ID', status=400)

    new_gamedata.admin_name = user_obj

    return HttpResponse('Successfully registered')


# For development
def register_page_temp(request):
    return render(request, 'for_develop/reg_game_temp.html')


def register_game_data_temp(request):
    generator = KeyGenerator()

    new_gamedata = Gamedata()
    new_gamedata.game_name = request.POST['game_name']
    new_gamedata.score_type = request.POST['score_type']
    new_gamedata.api_key = generator.key_gen()
    new_gamedata.admin_name = 'temp'

    new_gamedata.save()

    return redirect(test)


def sync(request):
    income = json.dumps(request.body)

    # 예외처리
    if check_sync_data(income) is False:
        return JsonResponse({'message': 'Wrong or Missing key'}, status=400)

    new_ladder_data = Ladder()
    new_ladder_data.game_index = Gamedata.objects.find(income['api_key'])
    new_ladder_data.score = income['score']

    try:
        user_obj = User.objects.get(username=income['player_id'])
    except User.DoesNotExist:
        return JsonResponse({'message': 'Wrong User name'}, status=400)
    new_ladder_data.player_id = user_obj

    new_ladder_data.save()

    return JsonResponse({'message': 'Successfully synced'})


def test(request):
    all = Ladder.objects.all()
    all_game_data = Gamedata.objects.all()

    return render(request, 'gamedata/test.html', {'all_data': all, 'all_game_data': all_game_data})


def request_ladder_data(request):
    income = json.dumps(request.body)

    ladder_info_list = Ladder.objects.filter(player_id=income['player_id'])[:10]
    result = dict()
    for index, info in enumerate(ladder_info_list):
        result[index] = {'game_title': info.game_index.game_name, 'score': info.score}

    return JsonResponse(result)
