
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from apps.bursaries.models import Bursary, Bookmark
from apps.bursaries.recommendations import BursaryRecommendationEngine

def home_view(request):
    """Homepage with search and trending bursaries"""
    trending_bursaries = Bursary.objects.filter(
        status='active'
    ).order_by('-views_count', '-applications_count')[:6]
    
    # Get recommendations for logged-in users
    recommendations = []
    if request.user.is_authenticated:
        engine = BursaryRecommendationEngine(request.user)
        recommendations = engine.get_recommendations(limit=6)
    
    context = {
        'trending_bursaries': trending_bursaries,
        'recommendations': recommendations,
    }
    return render(request, 'pages/home.html', context)

def bursary_list_view(request):
    """Bursary listing with filters and search"""
    bursaries = Bursary.objects.filter(status='active')
    
    # Search
    query = request.GET.get('q')
    if query:
        bursaries = bursaries.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(provider_name__icontains=query)
        )
    
    # Filters
    category = request.GET.get('category')
    if category:
        bursaries = bursaries.filter(category=category)
    
    country = request.GET.get('country')
    if country:
        bursaries = bursaries.filter(country=country)
    
    education_level = request.GET.get('education_level')
    if education_level:
        bursaries = bursaries.filter(eligible_education_levels__icontains=education_level)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    bursaries = bursaries.order_by(sort)
    
    # Pagination
    paginator = Paginator(bursaries, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_category': category,
    }
    return render(request, 'bursaries/list.html', context)

def bursary_detail_view(request, slug):
    """Detailed bursary view"""
    bursary = get_object_or_404(Bursary, slug=slug)
    
    # Increment view count
    bursary.views_count += 1
    bursary.save(update_fields=['views_count'])
    
    # Check if bookmarked
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, bursary=bursary).exists()
    
    # Get similar bursaries
    similar = BursaryRecommendationEngine.get_similar_bursaries(bursary, limit=4)
    
    context = {
        'bursary': bursary,
        'is_bookmarked': is_bookmarked,
        'similar_bursaries': similar,
    }
    return render(request, 'bursaries/detail.html', context)

@login_required
def toggle_bookmark(request, slug):
    """Toggle bookmark status"""
    bursary = get_object_or_404(Bursary, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, bursary=bursary)
    
    if not created:
        bookmark.delete()
        messages.success(request, 'Bookmark removed.')
    else:
        messages.success(request, 'Bursary bookmarked!')
    
    return redirect('bursaries:detail', slug=slug)

@login_required
def bookmarks_view(request):
    """User's bookmarked bursaries"""
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('bursary')
    
    context = {'bookmarks': bookmarks}
    return render(request, 'bursaries/bookmarks.html', context)
