
# Register your models here.

from django.contrib import admin
from django.utils.html import format_html
from apps.bursaries.models import Bursary, Bookmark

@admin.register(Bursary)
class BursaryAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider_name', 'category', 'amount_display', 
                   'deadline', 'status_badge', 'views_count', 'applications_count']
    list_filter = ['status', 'category', 'country', 'created_at']
    search_fields = ['title', 'provider_name', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'applications_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'status')
        }),
        ('Financial Details', {
            'fields': ('amount', 'currency')
        }),
        ('Eligibility', {
            'fields': ('eligible_education_levels', 'eligible_fields', 'min_gpa')
        }),
        ('Location', {
            'fields': ('country', 'city')
        }),
        ('Organization', {
            'fields': ('provider_name', 'provider_website', 'contact_email')
        }),
        ('Dates & Application', {
            'fields': ('application_deadline', 'start_date', 'application_url', 'required_documents')
        }),
        ('Metadata', {
            'fields': ('views_count', 'applications_count', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount:,.2f}"
    amount_display.short_description = 'Amount'
    
    def deadline(self, obj):
        if obj.days_until_deadline <= 7:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', 
                             obj.application_deadline)
        return obj.application_deadline
    deadline.short_description = 'Deadline'
    
    def status_badge(self, obj):
        colors = {
            'active': 'green',
            'closed': 'red',
            'pending': 'orange'
        }
        color = colors.get(obj.status, 'gray')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 
                         color, obj.get_status_display())
    status_badge.short_description = 'Status'
    
    actions = ['approve_bursaries', 'close_bursaries']
    
    def approve_bursaries(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} bursaries approved.')
    approve_bursaries.short_description = 'Approve selected bursaries'
    
    def close_bursaries(self, request, queryset):
        updated = queryset.update(status='closed')
        self.message_user(request, f'{updated} bursaries closed.')
    close_bursaries.short_description = 'Close selected bursaries'

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'bursary', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'bursary__title']

