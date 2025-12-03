from django.contrib import admin
from apps.applications.models import ApplicationStatus, ApplicationDocument


@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'bursary', 'status', 'submitted_at', 'created_at']
    list_filter = ['status', 'created_at', 'submitted_at']
    search_fields = ['user__username', 'bursary__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'bursary', 'status')
        }),
        ('Application Content', {
            'fields': ('cover_letter', 'motivation', 'achievements')
        }),
        ('Dates', {
            'fields': ('submitted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'document_type', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['application__user__username', 'application__bursary__title']
    readonly_fields = ['uploaded_at']

