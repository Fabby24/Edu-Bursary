from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='student'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username}"


class StudentProfile(models.Model):
    """Extended profile for student users"""
    EDUCATION_LEVEL_CHOICES = (
        ('high_school', 'High School'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
    )
    
    YEAR_OF_STUDY_CHOICES = (
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
        ('5', 'Year 5'),
        ('other', 'Other'),
    )
    
    FINANCIAL_NEED_CHOICES = (
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    field_of_study = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    year_of_study = models.CharField(max_length=10, choices=YEAR_OF_STUDY_CHOICES, blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    financial_need = models.CharField(max_length=10, choices=FINANCIAL_NEED_CHOICES, default='medium')
    interests = models.TextField(blank=True, null=True, help_text="Your areas of interest, comma-separated")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
