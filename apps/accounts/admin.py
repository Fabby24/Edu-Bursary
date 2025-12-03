from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.accounts.models import User, StudentProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_staff', 'date_joined']
    list_filter = ['user_type', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone_number')
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'education_level', 'field_of_study', 'institution', 'gpa', 'country']
    list_filter = ['education_level', 'field_of_study', 'country', 'financial_need']
    search_fields = ['user__username', 'institution', 'city']
    readonly_fields = ['created_at', 'updated_at']

