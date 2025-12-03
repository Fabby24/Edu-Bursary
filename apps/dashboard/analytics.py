from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from apps.bursaries.models import Bursary
from apps.applications.models import ApplicationStatus
from apps.accounts.models import User, StudentProfile

class DashboardAnalytics:
    """Analytics service for admin dashboard"""
    
    @staticmethod
    def get_overview_stats():
        """Get high-level platform statistics"""
        total_bursaries = Bursary.objects.filter(status='active').count()
        total_students = User.objects.filter(user_type='student').count()
        total_applications = ApplicationStatus.objects.count()
        
        # Active bursaries with approaching deadlines (next 30 days)
        approaching_deadline = Bursary.objects.filter(
            status='active',
            application_deadline__lte=timezone.now().date() + timedelta(days=30),
            application_deadline__gte=timezone.now().date()
        ).count()
        
        return {
            'total_bursaries': total_bursaries,
            'total_students': total_students,
            'total_applications': total_applications,
            'approaching_deadline': approaching_deadline,
        }
    
    @staticmethod
    def get_bursary_performance():
        """Get performance metrics for bursaries"""
        bursaries = Bursary.objects.filter(status='active').annotate(
            application_count=Count('applications')
        ).order_by('-application_count')[:10]
        
        return bursaries
    
    @staticmethod
    def get_category_distribution():
        """Get bursary distribution by category"""
        categories = Bursary.objects.filter(status='active').values(
            'category'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        return list(categories)
    
    @staticmethod
    def get_application_trends(days=30):
        """Get application trends over time"""
        start_date = timezone.now() - timedelta(days=days)
        
        applications = ApplicationStatus.objects.filter(
            created_at__gte=start_date
        ).extra(
            select={'date': 'DATE(created_at)'}
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        return list(applications)
    
    @staticmethod
    def get_student_engagement():
        """Get student engagement metrics"""
        # Students with complete profiles
        complete_profiles = StudentProfile.objects.exclude(
            Q(institution='') | Q(gpa__isnull=True)
        ).count()
        
        total_profiles = StudentProfile.objects.count()
        
        # Active students (with applications or bookmarks)
        active_students = User.objects.filter(
            Q(applications__isnull=False) | Q(bookmarks__isnull=False)
        ).distinct().count()
        
        return {
            'complete_profiles': complete_profiles,
            'total_profiles': total_profiles,
            'active_students': active_students,
            'profile_completion_rate': round((complete_profiles / total_profiles * 100), 2) if total_profiles > 0 else 0
        }
    
    @staticmethod
    def get_popular_fields():
        """Get most popular fields of study"""
        fields = StudentProfile.objects.values(
            'field_of_study'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        return list(fields)
