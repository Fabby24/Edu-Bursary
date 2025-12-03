from django.db.models import Q, Count, F
from django.utils import timezone
from datetime import timedelta
from apps.bursaries.models import Bursary, Bookmark
from apps.applications.models import ApplicationStatus
from apps.accounts.models import StudentProfile

class BursaryRecommendationEngine:
    """
    Intelligent recommendation system that scores bursaries based on:
    1. Profile matching (40% weight)
    2. Trending/popularity (20% weight)
    3. Deadline urgency (20% weight)
    4. Past application patterns (20% weight)
    """
    
    def __init__(self, user):
        self.user = user
        # Use related_name `student_profile` and handle missing profile gracefully
        try:
            self.profile = user.student_profile
        except Exception:
            # Could be AttributeError or StudentProfile.DoesNotExist
            self.profile = None
    
    def get_recommendations(self, limit=10):
        """
        Main method to get personalized bursary recommendations
        Returns: QuerySet of recommended bursaries with scores
        """
        if not self.profile:
            # If no profile, return trending bursaries
            return self._get_trending_bursaries(limit)
        
        # Get active bursaries
        active_bursaries = Bursary.objects.filter(
            status='active',
            application_deadline__gte=timezone.now().date()
        ).exclude(
            # Exclude already applied
            applications__user=self.user
        ).exclude(
            # Exclude bookmarked (show separately)
            bookmarked_by__user=self.user
        )
        
        # Score each bursary
        scored_bursaries = []
        for bursary in active_bursaries:
            score = self._calculate_bursary_score(bursary)
            scored_bursaries.append((bursary, score))
        
        # Sort by score descending
        scored_bursaries.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N
        return [bursary for bursary, score in scored_bursaries[:limit]]
    
    def _calculate_bursary_score(self, bursary):
        """Calculate composite score for a bursary (0-100)"""
        profile_score = self._profile_match_score(bursary) * 0.40
        trending_score = self._trending_score(bursary) * 0.20
        urgency_score = self._deadline_urgency_score(bursary) * 0.20
        pattern_score = self._application_pattern_score(bursary) * 0.20
        
        total_score = profile_score + trending_score + urgency_score + pattern_score
        return round(total_score, 2)
    
    def _profile_match_score(self, bursary):
        """
        Score based on how well bursary matches student profile (0-100)
        """
        score = 0
        max_score = 100
        
        # Education level match (30 points)
        eligible_levels = [level.strip() for level in bursary.eligible_education_levels.split(',')]
        if self.profile.education_level in eligible_levels:
            score += 30
        
        # Field of study match (30 points)
        eligible_fields = [field.strip() for field in bursary.eligible_fields.split(',')]
        if self.profile.field_of_study in eligible_fields:
            score += 30
        
        # GPA requirement (20 points)
        if bursary.min_gpa:
            if self.profile.gpa and self.profile.gpa >= bursary.min_gpa:
                score += 20
            # Partial points if close
            elif self.profile.gpa and self.profile.gpa >= (bursary.min_gpa - 0.3):
                score += 10
        else:
            score += 20  # No GPA requirement = full points
        
        # Location match (10 points)
        if bursary.country == self.profile.country:
            score += 10
        
        # Financial need match (10 points)
        if bursary.category == 'need' and self.profile.financial_need:
            score += 10
        elif bursary.category != 'need':
            score += 5  # Neutral for non-need based
        
        return min(score, max_score)
    
    def _trending_score(self, bursary):
        """
        Score based on popularity/trending (0-100)
        Factors: views, bookmarks, applications
        """
        # Normalize views (assume max 1000 views is 100%)
        views_score = min((bursary.views_count / 1000) * 40, 40)
        
        # Count bookmarks (assume max 50 bookmarks is 100%)
        bookmark_count = bursary.bookmarked_by.count()
        bookmark_score = min((bookmark_count / 50) * 30, 30)
        
        # Applications count (assume max 100 applications is 100%)
        app_score = min((bursary.applications_count / 100) * 30, 30)
        
        return views_score + bookmark_score + app_score
    
    def _deadline_urgency_score(self, bursary):
        """
        Score based on how soon deadline is (0-100)
        More urgent = higher score (encourages action)
        """
        days_left = bursary.days_until_deadline
        
        if days_left <= 0:
            return 0
        elif days_left <= 7:
            return 100  # Very urgent
        elif days_left <= 14:
            return 80
        elif days_left <= 30:
            return 60
        elif days_left <= 60:
            return 40
        else:
            return 20  # Plenty of time
    
    def _application_pattern_score(self, bursary):
        """
        Score based on similar application patterns (0-100)
        Look at what similar students applied to
        """
        # Get user's past applications
        user_apps = ApplicationStatus.objects.filter(user=self.user).values_list('bursary', flat=True)
        
        if not user_apps:
            return 50  # Neutral score for new users
        
        # Find users who applied to similar bursaries
        similar_users = ApplicationStatus.objects.filter(
            bursary__in=user_apps
        ).exclude(
            user=self.user
        ).values_list('user', flat=True).distinct()
        
        if not similar_users:
            return 50
        
        # Count how many similar users applied to this bursary
        similar_applications = ApplicationStatus.objects.filter(
            user__in=similar_users,
            bursary=bursary
        ).count()
        
        # Normalize (assume 10 similar applications = 100%)
        score = min((similar_applications / 10) * 100, 100)
        
        return score if score > 0 else 30  # Minimum 30 points
    
    def _get_trending_bursaries(self, limit):
        """
        Fallback method for users without profiles
        Returns most popular active bursaries
        """
        return Bursary.objects.filter(
            status='active',
            application_deadline__gte=timezone.now().date()
        ).annotate(
            popularity=F('views_count') + F('applications_count') * 2
        ).order_by('-popularity')[:limit]
    
    @staticmethod
    def get_similar_bursaries(bursary, limit=5):
        """
        Get bursaries similar to a given bursary
        Based on: category, field, education level
        """
        similar = Bursary.objects.filter(
            status='active',
            application_deadline__gte=timezone.now().date()
        ).exclude(
            id=bursary.id
        ).filter(
            Q(category=bursary.category) |
            Q(eligible_fields__icontains=bursary.eligible_fields.split(',')[0]) |
            Q(country=bursary.country)
        ).distinct()[:limit]
        
        return similar