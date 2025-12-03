from django.urls import path
from apps.applications import views

app_name = 'applications'

urlpatterns = [
    path('tracker/', views.application_tracker_view, name='tracker'),
    path('add/<int:bursary_id>/', views.add_application, name='add'),
    path('update/<int:application_id>/', views.update_application_status, name='update'),
    path('upload/<int:application_id>/', views.upload_document, name='upload'),
]