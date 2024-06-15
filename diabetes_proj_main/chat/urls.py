from django.urls import path
from .views import render_chat, send_message, load_messages

urlpatterns = [
    path('dialog/<int:sender_id>/<int:receiver_id>', render_chat, name='chat'),
    path('send-message/', send_message, name='send_message'),
    path('load-messages/<int:sender_id>/<int:receiver_id>/', load_messages, name='load_message'),
]