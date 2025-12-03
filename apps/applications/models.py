from django.db import models
from django.core.validators import FileExtensionValidator
from apps.accounts.models import User
from apps.bursaries.models import Bursary


class ApplicationStatus(models.Model):
    """Model for tracking bursary applications"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    bursary = models.ForeignKey(Bursary, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Application Details
    cover_letter = models.TextField()
    motivation = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    
    # Dates
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'bursary')
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.bursary.title}"


class ApplicationDocument(models.Model):
    """Model for storing application documents"""
    DOCUMENT_TYPES = (
        ('transcript', 'Academic Transcript'),
        ('id', 'ID Document'),
        ('proof_of_address', 'Proof of Address'),
        ('recommendation_letter', 'Recommendation Letter'),
        ('essay', 'Essay'),
        ('certificate', 'Certificate'),
        ('other', 'Other'),
    )
    
    application = models.ForeignKey(ApplicationStatus, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=25, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to='applications/documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Application Document'
        verbose_name_plural = 'Application Documents'
    
    def __str__(self):
        return f"{self.application} - {self.get_document_type_display()}"
