from django.contrib import admin
from apps.dashboard.models import DashboardMetric, UserActivity


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'value', 'last_updated']
    readonly_fields = ['last_updated']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__username', 'description']
    readonly_fields = ['timestamp']
