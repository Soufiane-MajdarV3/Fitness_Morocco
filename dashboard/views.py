from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from datetime import timedelta
from django.utils import timezone
from bookings.models import Booking, Review
from clients.models import ClientProfile, ClientProgress
from trainers.models import Trainer


@login_required
def client_dashboard_view(request):
    if request.user.user_type != 'client':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    try:
        client_profile = ClientProfile.objects.get(user=request.user)
    except ClientProfile.DoesNotExist:
        client_profile = ClientProfile.objects.create(user=request.user)
    
    # Get bookings
    upcoming_bookings = Booking.objects.filter(
        client=request.user,
        booking_date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    ).order_by('booking_date', 'start_time')
    
    completed_bookings = Booking.objects.filter(
        client=request.user,
        status='completed'
    ).order_by('-booking_date')[:5]
    
    # Statistics
    total_sessions = Booking.objects.filter(client=request.user, status='completed').count()
    total_spent = Booking.objects.filter(client=request.user).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Progress
    progress_records = ClientProgress.objects.filter(client=client_profile).order_by('-date')[:10]
    
    context = {
        'client_profile': client_profile,
        'upcoming_bookings': upcoming_bookings,
        'completed_bookings': completed_bookings,
        'total_sessions': total_sessions,
        'total_spent': total_spent,
        'progress_records': progress_records,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def trainer_dashboard_view(request):
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    try:
        trainer = Trainer.objects.get(user=request.user)
    except Trainer.DoesNotExist:
        trainer = Trainer.objects.create(
            user=request.user,
            price_per_hour=0
        )
    
    # Get bookings
    upcoming_bookings = Booking.objects.filter(
        trainer=trainer,
        booking_date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    ).order_by('booking_date', 'start_time')
    
    completed_bookings = Booking.objects.filter(
        trainer=trainer,
        status='completed'
    ).order_by('-booking_date')[:5]
    
    # Statistics
    total_sessions = Booking.objects.filter(trainer=trainer, status='completed').count()
    total_earnings = Booking.objects.filter(trainer=trainer, status='completed').aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Reviews
    reviews = Review.objects.filter(trainer=trainer).order_by('-created_at')[:5]
    avg_rating = trainer.rating
    total_reviews = trainer.total_reviews
    
    # Monthly earnings (last 30 days)
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    monthly_earnings = Booking.objects.filter(
        trainer=trainer,
        status='completed',
        updated_at__date__gte=thirty_days_ago
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    context = {
        'trainer': trainer,
        'upcoming_bookings': upcoming_bookings,
        'completed_bookings': completed_bookings,
        'total_sessions': total_sessions,
        'total_earnings': total_earnings,
        'monthly_earnings': monthly_earnings,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
    }
    
    return render(request, 'trainer_dashboard.html', context)
