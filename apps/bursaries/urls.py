from django.urls import path
from apps.bursaries import views

app_name = 'bursaries'

urlpatterns = [
    path('', views.bursary_list_view, name='list'),
    path('<slug:slug>/', views.bursary_detail_view, name='detail'),
    path('<slug:slug>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('my/bookmarks/', views.bookmarks_view, name='bookmarks'),
]
