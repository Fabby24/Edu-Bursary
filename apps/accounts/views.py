

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.forms import StudentSignupForm, StudentProfileForm
from apps.accounts.models import StudentProfile

def signup_view(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'student'
            user.save()
            
            # Create empty profile
            StudentProfile.objects.create(
                user=user,
                education_level='bachelor',
                field_of_study='other',
                country='Unknown',
                city='Unknown'
            )
            
            login(request, user)
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('accounts:profile')
    else:
        form = StudentSignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request):
    try:
        profile = request.user.student_profile
    except StudentProfile.DoesNotExist:
        profile = StudentProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})
