from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
import json

from Users.models import Client,CustomUser,GameOrder
from .models import Game,Rank,GameRankAssociation
from Users.verification import user_is_buster, user_valid
from Messages.models import Message


@user_is_buster
@user_valid
@login_required
def games_page(request,**kwargs):
    games_list = list(Game.objects.all().values())
    for game in games_list:
        game['ranks'] = {rank.id: {'value':rank.rank_value,'order':rank.order,'img':rank.rank_img} for rank in list(Rank.objects.filter(game__id=game['id']))}
    return render(request, 'Games_page.html',{"Games":games_list, **kwargs})



