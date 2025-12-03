from django.urls import path
from apps.chatbot import views

app_name = 'chatbot'

urlpatterns = [
    path('interface/', views.chatbot_interface, name='interface'),
    path('message/', views.chatbot_message, name='message'),
    path('history/<str:session_id>/', views.get_conversation_history, name='history'),
]