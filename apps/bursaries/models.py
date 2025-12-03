from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User


class Bursary(models.Model):
    """Model for bursary opportunities"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
    )
    
    CATEGORY_CHOICES = (
        ('merit', 'Merit-Based'),
        ('need', 'Need-Based'),
        ('demographic', 'Demographic-Based'),
        ('subject', 'Subject-Specific'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Financial Details
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Eligibility Requirements
    eligible_education_levels = models.TextField(help_text="Comma-separated values")
    eligible_fields = models.TextField(help_text="Comma-separated values")
    min_gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    # Location
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    # Provider Information
    provider_name = models.CharField(max_length=200)
    provider_website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Application Details
    application_deadline = models.DateField()
    start_date = models.DateField(null=True, blank=True)
    application_url = models.URLField(blank=True, null=True)
    required_documents = models.TextField(blank=True, null=True)
    
    # Metadata
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bursaries_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Bursary'
        verbose_name_plural = 'Bursaries'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def days_until_deadline(self):
        """Returns days remaining until application deadline"""
        return (self.application_deadline - timezone.now().date()).days
    
    @property
    def is_deadline_passed(self):
        """Check if deadline has passed"""
        return self.application_deadline < timezone.now().date()


class Bookmark(models.Model):
    """Model for bookmarked bursaries"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    bursary = models.ForeignKey(Bursary, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'bursary')
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.bursary.title}"
