from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='receive_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    message_text = models.TextField(max_length=2000, blank=False, null=False)