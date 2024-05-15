from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from Users.models import Client,CustomUser,GameOrder,Payment,Orders
from .models import Game,Rank,GameRankAssociation
from Messages.models import Message

@login_required
@require_POST
def get_game_rank_by_game_id(request):
    """Try to get game rank by game id and send it to the user"""
    game_id = request.POST.get('game_id')
    if not game_id:
        return JsonResponse({'success': False, 'message': 'No game id provided'}, status=400)
    game = get_object_or_404(Game, id=game_id)
    try:
        list_of_ranks = list(Rank.objects.filter(game=game).values())
        if list_of_ranks:
            response_data = {'success': True, 'message': 'Ranks found', 'data': list_of_ranks, 'id': game.id}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': True, 'message': 'Ranks not found! Using numerical values', 'id': game.id})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'message': 'Game not found'}, status=404)
    except Exception as error:
        return JsonResponse({'success': False, 'message': f'Server Error {error}'}, status=500)


@login_required
def buy_boost(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        game_id = data.get('game_id')
        rank_from = data.get('rank_from')
        rank_to = data.get('rank_to')
        value = data.get('boost_value')
        description = data.get('boost_description')
        user_client = Client.objects.get(user=request.user)
        try:
            from_rank = Rank.objects.get(game_id=game_id, rank_value=rank_from)
            to_rank = Rank.objects.get(game_id=game_id, rank_value=rank_to)
            GameOrder.objects.create(client=user_client,
                                     GameRankAssociation=GameRankAssociation.objects.create(game_id=game_id,
                                                                                            from_rank=from_rank,
                                                                                            to_rank=to_rank),
                                     order_payment_value=value,
                                     order_payment_description=description)
            return JsonResponse({'success': True})
        except Exception as error:
            print(error)
            return JsonResponse({'success': False, 'message': str(error)})
    return JsonResponse({'success': False, 'message': 'Invalid request method or form data missing'})


@login_required
def accept_order(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        payment_client = data.get('payment_client')
        receiver = Client.objects.get(user=CustomUser.objects.get(username=payment_client))
        sender = Client.objects.get(user=request.user)
        if receiver != sender:
            payment_value = data.get('payment_value')
            payment_description = data.get('payment_description')
            order_id = data.get('order_id')
            order = GameOrder.objects.get(id=order_id)
            content = (f"Hi, im {sender.user.username}, and i take you order with id {order_id}."
                       f" Order value is {payment_value}"
                       f" Order description is {payment_description}")
            Pay_order = Payment(amount=order.order_payment_value)
            Pay_order.save()
            Main_order = Orders(client=sender,booster=receiver,order_payment_data=Pay_order)
            Main_order.save()
            order.delete()
            message = Message(sender=sender,receiver=receiver,content=content)
            message.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': "Client and booster cant be one person!"})