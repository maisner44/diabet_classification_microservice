from django.http import JsonResponse
from .models import ChatMessage
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
import json

def render_chat(request, sender_id, receiver_id):
    sender = get_object_or_404(User, pk=sender_id)
    receiver = get_object_or_404(User, pk=receiver_id)
    context = {
        'sender': sender,
        'receiver': receiver,
        'sender_id': sender.id,
        'receiver_id': receiver.id,
    }
    return render(request, 'chat/chat.html', context)


@require_POST
def send_message(request):
    data = json.loads(request.body)
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message_text = data.get('message_text')

    if sender_id and receiver_id and message_text:
        sender = get_object_or_404(User, pk=sender_id)
        receiver = get_object_or_404(User, pk=receiver_id)

        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message_text=message_text
        )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

   
def load_messages(request, sender_id, receiver_id):
    sender_receiver_messages = ChatMessage.objects.filter(sender_id=sender_id, receiver_id=receiver_id)
    receiver_sender_messages = ChatMessage.objects.filter(sender_id=receiver_id, receiver_id=sender_id)

    all_messages = list(sender_receiver_messages) + list(receiver_sender_messages)

    sorted_messages = sorted(all_messages, key=lambda message: message.timestamp)
    message_list = [
        {
            'sender_id': message.sender_id,
            'sender_username': message.sender.username,
            'recipient_username': message.receiver.username,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'content': message.message_text,
        }
        for message in sorted_messages
    ]
    return JsonResponse({'messages': message_list})
