# AI INTEGRATION SERVICE
# This module handles interactions with AI services for the chatbot functionality.
import json
import uuid
from django.conf import settings
from apps.bursaries.models import Bursary
from apps.accounts.models import StudentProfile
import requests

class ChatbotAIService:
    """
    Service to handle AI chatbot interactions
    Supports Google Generative AI (Gemini) - Free tier
    """
    
    def __init__(self, user=None):
        self.user = user
        self.model = getattr(settings, 'CHATBOT_MODEL', 'google')
        self.api_key = self._get_api_key()
    
    def _get_api_key(self):
        """Get Google API key"""
        return getattr(settings, 'GOOGLE_API_KEY', '')
    
    def generate_system_prompt(self):
        """
        Create personalized system prompt based on user profile
        """
        base_prompt = """You are an intelligent bursary and scholarship assistant for an education funding platform. 
        Your role is to help students:
        1. Find suitable bursaries and scholarships
        2. Understand eligibility requirements
        3. Get guidance on application processes
        4. Understand deadlines and important dates
        5. Provide step-by-step application help
        
        Be friendly, encouraging, and provide accurate information.
        If asked about specific bursaries, provide details from the database.
        Always encourage students to apply and not give up."""
        
        # Add user context if available
        if self.user and hasattr(self.user, 'student_profile'):
            profile = self.user.student_profile
            user_context = f"""
            
            User Profile Context:
            - Education Level: {profile.get_education_level_display()}
            - Field of Study: {profile.field_of_study}
            - Institution: {profile.institution or 'Not specified'}
            - Country: {profile.country}
            - GPA: {profile.gpa or 'Not specified'}
            
            Use this context to provide personalized recommendations.
            """
            base_prompt += user_context
        
        return base_prompt
    
    def get_relevant_bursaries(self, query):
        """
        Search for relevant bursaries based on user query
        Returns: List of bursary objects
        """
        from django.db.models import Q
        
        # Simple keyword search
        bursaries = Bursary.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(provider_name__icontains=query),
            status='active'
        )[:5]
        
        return bursaries
    
    def format_bursary_info(self, bursaries):
        """Format bursary information for AI context"""
        if not bursaries:
            return "No matching bursaries found in the database."
        
        info = "Here are relevant bursaries from our database:\n\n"
        for bursary in bursaries:
            info += f"""
            Title: {bursary.title}
            Provider: {bursary.provider_name}
            Category: {bursary.get_category_display()}
            Amount: {bursary.currency} {bursary.amount:,.2f}
            Deadline: {bursary.application_deadline}
            Eligibility: {bursary.eligible_education_levels}
            Description: {bursary.description[:200]}...
            
            """
        return info
    
    def call_google_api(self, messages, conversation_history=None):
        """
        Call Google Generative AI (Gemini) API - Free tier available
        Documentation: https://ai.google.dev
        Uses gemini-2.5-flash (latest stable free model)
        """
        api_key = self.api_key or getattr(settings, 'GOOGLE_API_KEY', '')

        if not api_key:
            return "Chat service is not configured. Please set GOOGLE_API_KEY in settings or environment."

        # Use v1 endpoint with gemini-2.5-flash model
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

        # Build message list
        api_messages = [
            {"role": "user", "parts": [{"text": self.generate_system_prompt()}]},
        ]

        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                role = "user" if msg.sender == "user" else "model"
                api_messages.append({
                    "role": role,
                    "parts": [{"text": msg.message}]
                })

        # Add current message
        api_messages.append({
            "role": "user",
            "parts": [{"text": messages}]
        })

        payload = {
            "contents": api_messages,
            "generationConfig": {
                "maxOutputTokens": 1000,
                "temperature": 0.7,
                "topP": 0.8,
                "topK": 10
            }
        }

        headers = {
            "Content-Type": "application/json",
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # Extract response from Google Generative AI format
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    if len(candidate["content"]["parts"]) > 0:
                        return candidate["content"]["parts"][0]["text"]

            # Fallback: return error message with details
            return f"Unexpected response format: {json.dumps(data)}"

        except requests.exceptions.RequestException as e:
            return f"Sorry, I encountered an error contacting Google API: {str(e)}"
        except Exception as e:
            return f"Sorry, an unexpected error occurred: {str(e)}"
    
    def get_response(self, user_message, conversation_history=None):
        """
        Main method to get AI response
        Automatically searches for relevant bursaries if needed
        """
        # Check if message is asking about bursaries
        bursary_keywords = ['bursary', 'scholarship', 'grant', 'funding', 'financial aid']
        needs_bursary_search = any(keyword in user_message.lower() for keyword in bursary_keywords)
        
        enhanced_message = user_message
        
        if needs_bursary_search:
            # Search for relevant bursaries
            bursaries = self.get_relevant_bursaries(user_message)
            bursary_context = self.format_bursary_info(bursaries)
            
            # Add bursary context to message
            enhanced_message = f"{user_message}\n\n[Database Context]\n{bursary_context}"
        
        # Call Google Gemini API
        return self.call_google_api(enhanced_message, conversation_history) 

