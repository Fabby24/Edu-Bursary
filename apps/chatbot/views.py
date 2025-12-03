
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import uuid
from apps.chatbot.models import ChatConversation, ChatMessage
from apps.chatbot.ai_service import ChatbotAIService

@login_required
def chatbot_interface(request):
    """Render chatbot interface (optional full-page view)"""
    return render(request, 'chatbot/interface.html')

@login_required
@csrf_exempt
def chatbot_message(request):
    """
    API endpoint to handle chat messages
    POST: Send message and get AI response
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id')
            
            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            # Get or create conversation
            if session_id:
                try:
                    conversation = ChatConversation.objects.get(session_id=session_id, user=request.user)
                except ChatConversation.DoesNotExist:
                    conversation = ChatConversation.objects.create(
                        user=request.user,
                        session_id=str(uuid.uuid4())
                    )
            else:
                conversation = ChatConversation.objects.create(
                    user=request.user,
                    session_id=str(uuid.uuid4())
                )
            
            # Save user message
            ChatMessage.objects.create(
                conversation=conversation,
                sender='user',
                message=user_message
            )
            
            # Get conversation history (last 10 messages)
            history = conversation.messages.order_by('-timestamp')[:10][::-1]
            
            # Get AI response
            ai_service = ChatbotAIService(user=request.user)
            bot_response = ai_service.get_response(user_message, conversation_history=history)
            
            # Save bot response
            ChatMessage.objects.create(
                conversation=conversation,
                sender='bot',
                message=bot_response
            )
            
            return JsonResponse({
                'success': True,
                'response': bot_response,
                'session_id': conversation.session_id
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def get_conversation_history(request, session_id):
    """Get full conversation history"""
    try:
        conversation = ChatConversation.objects.get(session_id=session_id, user=request.user)
        messages = conversation.messages.all().values('sender', 'message', 'timestamp')
        
        return JsonResponse({
            'success': True,
            'messages': list(messages)
        })
    except ChatConversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)


