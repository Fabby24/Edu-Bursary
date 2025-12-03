
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.applications.models import ApplicationStatus, ApplicationDocument
from apps.bursaries.models import Bursary

@login_required
def application_tracker_view(request):
    """View all user applications"""
    applications = ApplicationStatus.objects.filter(
        user=request.user
    ).select_related('bursary').order_by('-updated_at')
    
    # Group by status
    draft = applications.filter(status='draft')
    submitted = applications.filter(status='submitted')
    under_review = applications.filter(status='under_review')
    accepted = applications.filter(status='accepted')
    rejected = applications.filter(status='rejected')
    
    context = {
        'applications': applications,
        'draft': draft,
        'submitted': submitted,
        'under_review': under_review,
        'accepted': accepted,
        'rejected': rejected,
    }
    return render(request, 'applications/tracker.html', context)

@login_required
def add_application(request, bursary_id):
    """Add bursary to application tracker"""
    bursary = get_object_or_404(Bursary, id=bursary_id)
    
    application, created = ApplicationStatus.objects.get_or_create(
        user=request.user,
        bursary=bursary,
        defaults={'status': 'draft'}
    )
    
    if created:
        messages.success(request, f'Added {bursary.title} to your tracker!')
    else:
        messages.info(request, 'This bursary is already in your tracker.')
    
    return redirect('applications:tracker')

@login_required
def update_application_status(request, application_id):
    """Update application status"""
    application = get_object_or_404(ApplicationStatus, id=application_id, user=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        cover_letter = request.POST.get('cover_letter', '')
        
        application.status = new_status
        application.cover_letter = cover_letter
        if new_status == 'submitted':
            application.submitted_at = timezone.now()
        application.save()
        
        messages.success(request, 'Application status updated!')
        return redirect('applications:tracker')
    
    return redirect('applications:tracker')

@login_required
def upload_document(request, application_id):
    """Upload document for application"""
    application = get_object_or_404(ApplicationStatus, id=application_id, user=request.user)
    
    if request.method == 'POST' and request.FILES.get('document'):
        doc_file = request.FILES['document']
        doc_type = request.POST.get('document_type', 'other')
        
        ApplicationDocument.objects.create(
            application=application,
            document_type=doc_type,
            file=doc_file,
        )
        
        messages.success(request, 'Document uploaded successfully!')
    
    return redirect('applications:tracker')

