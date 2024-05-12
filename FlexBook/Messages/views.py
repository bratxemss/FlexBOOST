from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Users.models import Client
from Users.verification import user_is_buster, user_valid
from .models import Message


@user_is_buster
@user_valid
@login_required
def messenger_page(request, **kwargs):
    """Creating and sending data about messages to 'Messenger.html'"""
    current_user = Client.objects.get(user=request.user)
    user_messages = {}
    received_messages = Message.objects.filter(receiver=current_user)
    sent_messages = Message.objects.filter(sender=current_user)

    for message in received_messages:
        timestamp_obj = message.timestamp
        timestamp = timestamp_obj.strftime("(%d.%m) %H:%M:%S")
        sender_username = message.sender.user.username
        chat_key = (message.sender, current_user)
        if chat_key not in user_messages:
            user_messages[chat_key] = []
        user_messages[chat_key].append({
            'id': message.id,
            'content': message.content,
            'sender': sender_username,
            'is_sent_by_user': False,
            'timestamp': timestamp,
        })

    for message in sent_messages:
        timestamp_obj = message.timestamp
        timestamp = timestamp_obj.strftime("(%d.%m) %H:%M:%S")
        chat_key = (message.receiver, current_user)
        if chat_key not in user_messages:
            user_messages[chat_key] = []
        user_messages[chat_key].append({
            'id': message.id,
            'content': message.content,
            'sender': current_user.user.username,
            'is_sent_by_user': True,
            'timestamp': timestamp,
        })

    for messages in user_messages.values():
        messages.sort(key=lambda x: datetime.strptime(x['timestamp'], "(%d.%m) %H:%M:%S"))

    for (user1, user2), messages in user_messages.items():
        user_messages[(user1, user2)] = messages
    return render(request, 'Messenger_page.html', {'user_messages': user_messages, **kwargs})
