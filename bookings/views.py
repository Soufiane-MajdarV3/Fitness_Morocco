from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from decimal import Decimal
from .models import Booking, Review, Payment
from .forms import BookingForm, ReviewForm, PaymentForm
from trainers.models import Trainer


@login_required
def booking_view(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
    except Trainer.DoesNotExist:
        return redirect('trainers')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.trainer = trainer
            # Calculate price
            duration_hours = booking.duration_minutes / 60
            booking.total_price = trainer.price_per_hour * Decimal(duration_hours)
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {
        'form': form,
        'trainer': trainer,
    })


@login_required
def booking_confirmation_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, client=request.user)
    except Booking.DoesNotExist:
        return redirect('home')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_price
            payment.status = 'completed'  # Simplified - no actual payment processing
            payment.save()
            
            booking.status = 'confirmed'
            booking.save()
            
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = PaymentForm()
    
    return render(request, 'booking_confirmation.html', {
        'booking': booking,
        'form': form,
    })


@login_required
def booking_success_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, client=request.user)
    except Booking.DoesNotExist:
        return redirect('home')
    
    return render(request, 'booking_success.html', {'booking': booking})


@login_required
def booking_list_view(request):
    if request.user.user_type == 'client':
        bookings = Booking.objects.filter(client=request.user).order_by('-booking_date')
    else:
        try:
            bookings = Booking.objects.filter(trainer__user=request.user).order_by('-booking_date')
        except:
            bookings = []
    
    return render(request, 'bookings_list.html', {'bookings': bookings})


@login_required
def add_review_view(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, client=request.user, status='completed')
    except Booking.DoesNotExist:
        return redirect('booking_list')
    
    # Check if review already exists
    if hasattr(booking, 'review'):
        return redirect('booking_list')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.trainer = booking.trainer
            review.client = request.user
            review.save()
            
            # Update trainer rating
            trainer = booking.trainer
            reviews = trainer.reviews.all()
            avg_rating = sum(r.rating for r in reviews) / reviews.count() if reviews.exists() else 0
            trainer.rating = avg_rating
            trainer.total_reviews = reviews.count()
            trainer.save()
            
            return redirect('booking_list')
    else:
        form = ReviewForm()
    
    return render(request, 'add_review.html', {
        'form': form,
        'booking': booking,
    })
