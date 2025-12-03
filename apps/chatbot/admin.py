
from django.contrib import admin
from apps.chatbot.models import ChatConversation, ChatMessage

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_id', 'message_count', 'started_at', 'last_message_at']
    list_filter = ['started_at', 'last_message_at']
    search_fields = ['user__username', 'session_id']
    readonly_fields = ['started_at', 'last_message_at']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'message_preview', 'timestamp']
    list_filter = ['sender', 'timestamp']
    search_fields = ['conversation__session_id', 'message']
    readonly_fields = ['timestamp']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

