from django.db import models
from apps.accounts.models import User


class DashboardMetric(models.Model):
    """Model for storing dashboard metrics and analytics"""
    METRIC_TYPES = (
        ('total_users', 'Total Users'),
        ('total_bursaries', 'Total Bursaries'),
        ('total_applications', 'Total Applications'),
        ('active_users_today', 'Active Users Today'),
        ('new_applications_today', 'New Applications Today'),
    )
    
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES, unique=True)
    value = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard Metric'
        verbose_name_plural = 'Dashboard Metrics'
    
    def __str__(self):
        return f"{self.get_metric_type_display()}: {self.value}"


class UserActivity(models.Model):
    """Model for tracking user activity"""
    ACTIVITY_TYPES = (
        ('login', 'Login'),
        ('view_bursary', 'View Bursary'),
        ('apply', 'Submit Application'),
        ('bookmark', 'Bookmark Bursary'),
        ('profile_update', 'Profile Update'),
        ('chat', 'Chat with Bot'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"
