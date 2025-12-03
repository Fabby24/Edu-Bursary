from django.db import models
from apps.accounts.models import User
import uuid


class ChatConversation(models.Model):
    """Model for storing chat conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_conversations')
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Chat Conversation'
        verbose_name_plural = 'Chat Conversations'
        ordering = ['-last_message_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.session_id}"


class ChatMessage(models.Model):
    """Model for storing individual chat messages"""
    SENDER_CHOICES = (
        ('user', 'User'),
        ('bot', 'Bot'),
    )
    
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.conversation.user.username} - {self.sender}"
