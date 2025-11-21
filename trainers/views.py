from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Trainer, TrainerAvailability, Certificate
from .forms import TrainerProfileUpdateForm, TrainerAvailabilityForm, CertificateForm
from bookings.models import Booking, Review


@login_required
def trainer_edit_profile(request):
    """Edit trainer profile"""
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    trainer = get_object_or_404(Trainer, user=request.user)
    
    if request.method == 'POST':
        form = TrainerProfileUpdateForm(request.POST, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('trainer_dashboard')
    else:
        form = TrainerProfileUpdateForm(instance=trainer)
    
    return render(request, 'trainer_edit_profile.html', {'form': form, 'trainer': trainer})


@login_required
def trainer_availability(request):
    """Manage trainer availability"""
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    trainer = get_object_or_404(Trainer, user=request.user)
    availabilities = TrainerAvailability.objects.filter(trainer=trainer).order_by('day_of_week', 'start_time')
    
    if request.method == 'POST':
        form = TrainerAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.trainer = trainer
            availability.save()
            return redirect('trainer_availability')
    else:
        form = TrainerAvailabilityForm()
    
    return render(request, 'trainer_availability.html', {
        'form': form,
        'availabilities': availabilities,
        'trainer': trainer
    })


@login_required
def delete_availability(request, availability_id):
    """Delete availability slot"""
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    availability = get_object_or_404(TrainerAvailability, id=availability_id, trainer__user=request.user)
    availability.delete()
    
    return redirect('trainer_availability')


@login_required
def trainer_my_clients(request):
    """View clients who booked sessions with trainer"""
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    trainer = get_object_or_404(Trainer, user=request.user)
    
    # Get unique clients who booked sessions
    clients = set()
    bookings = Booking.objects.filter(trainer=trainer).select_related('client')
    
    for booking in bookings:
        clients.add(booking.client)
    
    clients = list(clients)
    
    # Get client details with booking counts
    client_data = []
    for client in clients:
        booking_count = Booking.objects.filter(trainer=trainer, client=client).count()
        completed_count = Booking.objects.filter(trainer=trainer, client=client, status='completed').count()
        
        client_data.append({
            'user': client,
            'total_bookings': booking_count,
            'completed_sessions': completed_count,
        })
    
    return render(request, 'trainer_my_clients.html', {
        'trainer': trainer,
        'client_data': sorted(client_data, key=lambda x: x['completed_sessions'], reverse=True)
    })


@login_required
def trainer_earnings(request):
    """View trainer earnings and statistics"""
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    trainer = get_object_or_404(Trainer, user=request.user)
    
    # Total earnings
    total_earnings = Booking.objects.filter(
        trainer=trainer,
        status='completed'
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Monthly earnings
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    monthly_earnings = Booking.objects.filter(
        trainer=trainer,
        status='completed',
        updated_at__date__gte=thirty_days_ago
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Weekly earnings
    seven_days_ago = timezone.now().date() - timedelta(days=7)
    weekly_earnings = Booking.objects.filter(
        trainer=trainer,
        status='completed',
        updated_at__date__gte=seven_days_ago
    ).aggregate(total=Sum('total_price'))['total'] or 0
    
    # Sessions count
    total_sessions = Booking.objects.filter(trainer=trainer, status='completed').count()
    monthly_sessions = Booking.objects.filter(
        trainer=trainer,
        status='completed',
        updated_at__date__gte=thirty_days_ago
    ).count()
    
    # Average rating
    reviews = Review.objects.filter(trainer=trainer)
    avg_rating = reviews.aggregate(avg=Sum('rating') / Count('id'))['avg'] or 0 if reviews.exists() else 0
    
    # Monthly breakdown (last 6 months)
    monthly_data = []
    for i in range(5, -1, -1):
        month_start = timezone.now().date() - timedelta(days=30*i+30)
        month_end = timezone.now().date() - timedelta(days=30*i)
        
        month_earnings = Booking.objects.filter(
            trainer=trainer,
            status='completed',
            updated_at__date__gte=month_start,
            updated_at__date__lte=month_end
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        month_sessions = Booking.objects.filter(
            trainer=trainer,
            status='completed',
            updated_at__date__gte=month_start,
            updated_at__date__lte=month_end
        ).count()
        
        monthly_data.append({
            'month': month_end.strftime('%B'),
            'earnings': float(month_earnings),
            'sessions': month_sessions,
        })
    
    return render(request, 'trainer_earnings.html', {
        'trainer': trainer,
        'total_earnings': float(total_earnings),
        'monthly_earnings': float(monthly_earnings),
        'weekly_earnings': float(weekly_earnings),
        'total_sessions': total_sessions,
        'monthly_sessions': monthly_sessions,
        'avg_rating': round(avg_rating, 1),
        'monthly_data': monthly_data,
    })


@login_required
def trainer_bookings(request):
    """Manage trainer bookings"""
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    trainer = get_object_or_404(Trainer, user=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    
    if status_filter == 'pending':
        bookings = Booking.objects.filter(trainer=trainer, status='pending').order_by('booking_date')
    elif status_filter == 'confirmed':
        bookings = Booking.objects.filter(trainer=trainer, status='confirmed').order_by('booking_date')
    elif status_filter == 'completed':
        bookings = Booking.objects.filter(trainer=trainer, status='completed').order_by('-updated_at')
    elif status_filter == 'cancelled':
        bookings = Booking.objects.filter(trainer=trainer, status='cancelled').order_by('-updated_at')
    else:
        bookings = Booking.objects.filter(trainer=trainer).order_by('-created_at')
    
    # Statistics
    pending_count = Booking.objects.filter(trainer=trainer, status='pending').count()
    confirmed_count = Booking.objects.filter(trainer=trainer, status='confirmed').count()
    completed_count = Booking.objects.filter(trainer=trainer, status='completed').count()
    cancelled_count = Booking.objects.filter(trainer=trainer, status='cancelled').count()
    
    return render(request, 'trainer_bookings.html', {
        'trainer': trainer,
        'bookings': bookings,
        'status_filter': status_filter,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
    })


@login_required
def update_booking_status(request, booking_id):
    """Update booking status"""
    if request.user.user_type != 'trainer':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    booking = get_object_or_404(Booking, id=booking_id, trainer__user=request.user)
    new_status = request.POST.get('status')
    
    if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
        booking.status = new_status
        booking.save()
    
    return redirect('trainer_bookings')
