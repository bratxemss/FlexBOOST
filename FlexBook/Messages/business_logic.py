from datetime import datetime

from django.contrib.auth.decorators import login_required
import json
from Users.models import Client, CustomUser
from .models import Message
from django.http import JsonResponse
from django.utils import timezone

@login_required
def send_message(request):
    """Creating and saving message"""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        current_user = Client.objects.get(user=request.user)
        second_user = Client.objects.get(user=CustomUser.objects.get(username=data.get('second_name')))
        if current_user != second_user:
            message = data.get('message_value')
            current_time_utc = timezone.now()
            new_message = Message.objects.create(sender=current_user, receiver=second_user, content=message, timestamp=current_time_utc)
            message_timestamp = timezone.localtime(new_message.timestamp, second_user.user.timezone)
            timestamp = message_timestamp.strftime("(%d.%m) %H:%M:%S")
            if current_user.user.user_profile_pictures:
                return JsonResponse({'success': True, 'data': {
                    'message_timestamp': timestamp,
                    'sender_username': current_user.user.username,
                    'sender_avatar_url': current_user.user.user_profile_pictures,
                }})
            else:
                return JsonResponse({'success': True, 'data': {
                    'message_timestamp': timestamp,
                    'sender_username': current_user.user.username,
                    'sender_avatar_url': None,
                }})
        else:
            return JsonResponse({'success': False})