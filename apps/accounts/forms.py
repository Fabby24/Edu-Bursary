from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User, StudentProfile

class StudentSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'education_level', 'field_of_study', 'institution', 
            'year_of_study', 'gpa', 'country', 'city', 
            'financial_need', 'interests', 'bio', 'profile_picture'
        ]
        widgets = {
            'interests': forms.Textarea(attrs={'rows': 3}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }