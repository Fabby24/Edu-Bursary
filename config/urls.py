from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.bursaries.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),

    path('accounts/', include('apps.accounts.urls')),

    path('bursaries/', include('apps.bursaries.urls')),

    path('applications/', include('apps.applications.urls')),

    path('chatbot/', include('apps.chatbot.urls')),
    
    path('dashboard/', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
