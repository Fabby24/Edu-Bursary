
# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import csv
from datetime import datetime

from apps.dashboard.analytics import DashboardAnalytics
from apps.bursaries.models import Bursary
from apps.accounts.models import User
from apps.applications.models import ApplicationStatus

@staff_member_required
def dashboard_home(request):
    """Main admin dashboard"""
    analytics = DashboardAnalytics()
    
    overview = analytics.get_overview_stats()
    top_bursaries = analytics.get_bursary_performance()
    categories = analytics.get_category_distribution()
    engagement = analytics.get_student_engagement()
    popular_fields = analytics.get_popular_fields()
    
    context = {
        'overview': overview,
        'top_bursaries': top_bursaries,
        'categories': categories,
        'engagement': engagement,
        'popular_fields': popular_fields,
    }
    
    return render(request, 'dashboard/admin_home.html', context)

@staff_member_required
def analytics_view(request):
    """Detailed analytics page"""
    analytics = DashboardAnalytics()
    
    # Get trends data
    days = int(request.GET.get('days', 30))
    trends = analytics.get_application_trends(days)
    
    context = {
        'trends': trends,
        'selected_days': days,
    }
    
    return render(request, 'dashboard/analytics.html', context)

@staff_member_required
def manage_bursaries(request):
    """Manage all bursaries"""
    status_filter = request.GET.get('status', 'all')
    
    bursaries = Bursary.objects.all()
    
    if status_filter != 'all':
        bursaries = bursaries.filter(status=status_filter)
    
    bursaries = bursaries.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(bursaries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    
    return render(request, 'dashboard/manage_bursaries.html', context)

@staff_member_required
def approve_bursary(request, bursary_id):
    """Approve a pending bursary"""
    bursary = get_object_or_404(Bursary, id=bursary_id)
    bursary.status = 'active'
    bursary.save()
    
    messages.success(request, f'Bursary "{bursary.title}" has been approved.')
    return redirect('dashboard:manage_bursaries')

@staff_member_required
def reject_bursary(request, bursary_id):
    """Reject a pending bursary"""
    bursary = get_object_or_404(Bursary, id=bursary_id)
    bursary.status = 'closed'
    bursary.save()
    
    messages.warning(request, f'Bursary "{bursary.title}" has been rejected.')
    return redirect('dashboard:manage_bursaries')

@staff_member_required
def manage_users(request):
    """Manage platform users"""
    user_type = request.GET.get('type', 'all')
    
    users = User.objects.all()
    
    if user_type != 'all':
        users = users.filter(user_type=user_type)
    
    users = users.order_by('-date_joined')
    
    # Pagination
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'user_type': user_type,
    }
    
    return render(request, 'dashboard/manage_users.html', context)

@staff_member_required
def export_bursaries_csv(request):
    """Export bursaries to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="bursaries_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Title', 'Category', 'Provider', 'Amount', 'Currency', 
        'Deadline', 'Status', 'Views', 'Applications', 'Created'
    ])
    
    bursaries = Bursary.objects.all()
    
    for bursary in bursaries:
        writer.writerow([
            bursary.title,
            bursary.get_category_display(),
            bursary.provider_name,
            bursary.amount,
            bursary.currency,
            bursary.application_deadline,
            bursary.get_status_display(),
            bursary.views_count,
            bursary.applications_count,
            bursary.created_at.strftime('%Y-%m-%d')
        ])
    
    return response

@staff_member_required
def export_applications_csv(request):
    """Export applications to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="applications_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Student', 'Email', 'Bursary', 'Status', 'Applied Date', 'Updated'
    ])
    
    applications = ApplicationStatus.objects.select_related('user', 'bursary').all()
    
    for app in applications:
        writer.writerow([
            app.user.get_full_name() or app.user.username,
            app.user.email,
            app.bursary.title,
            app.get_status_display(),
            app.submitted_at.strftime('%Y-%m-%d %H:%M') if app.submitted_at else 'Not submitted',
            app.updated_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

@staff_member_required
def api_chart_data(request):
    """API endpoint for chart data (AJAX)"""
    chart_type = request.GET.get('type', 'categories')
    
    analytics = DashboardAnalytics()
    
    if chart_type == 'categories':
        data = analytics.get_category_distribution()
    elif chart_type == 'trends':
        days = int(request.GET.get('days', 30))
        data = analytics.get_application_trends(days)
    elif chart_type == 'fields':
        data = analytics.get_popular_fields()
    else:
        data = []
    
    return JsonResponse({'data': data})


