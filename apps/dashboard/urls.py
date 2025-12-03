from django.urls import path
from apps.dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('bursaries/', views.manage_bursaries, name='manage_bursaries'),
    path('bursaries/approve/<int:bursary_id>/', views.approve_bursary, name='approve_bursary'),
    path('bursaries/reject/<int:bursary_id>/', views.reject_bursary, name='reject_bursary'),
    path('users/', views.manage_users, name='manage_users'),
    path('export/bursaries/', views.export_bursaries_csv, name='export_bursaries'),
    path('export/applications/', views.export_applications_csv, name='export_applications'),
    path('api/chart-data/', views.api_chart_data, name='api_chart_data'),
]