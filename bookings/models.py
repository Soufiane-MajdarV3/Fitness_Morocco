from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from trainers.models import Trainer, SessionType

User = get_user_model()


class Booking(models.Model):
    """Session booking"""
    BOOKING_STATUSES = (
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'مؤكد'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغى'),
    )
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings',
                               limit_choices_to={'user_type': 'client'})
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='bookings')
    session_type = models.ForeignKey(SessionType, on_delete=models.SET_NULL, null=True)
    booking_date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.IntegerField(choices=[(30, '30 دقيقة'), (60, 'ساعة'), (90, 'ساعة ونصف'), (120, 'ساعتين')])
    status = models.CharField(max_length=20, choices=BOOKING_STATUSES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True)
    cancelled_by = models.CharField(max_length=20, choices=[('client', 'عميل'), ('trainer', 'مدرب')], blank=True)
    cancelled_reason = models.TextField(blank=True)
    
    # Commission tracking
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)  # Percentage (20 = 20%)
    commission_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # Platform commission
    trainer_earnings = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # Trainer gets after commission
    
    # Organization link (if trainer works for gym)
    organization = models.ForeignKey('payments.Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'الحجز'
        verbose_name_plural = 'الحجوزات'
        ordering = ['-booking_date']
        unique_together = ('trainer', 'booking_date', 'start_time')
    
    def __str__(self):
        return f"{self.client.get_full_name()} مع {self.trainer.user.get_full_name()}"
    
    def end_time(self):
        """Calculate end time"""
        from datetime import datetime, timedelta
        start = datetime.combine(self.booking_date, self.start_time)
        end = start + timedelta(minutes=self.duration_minutes)
        return end.time()


class Review(models.Model):
    """Client reviews of trainers"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='reviews')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given',
                               limit_choices_to={'user_type': 'client'})
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'تقييم'
        verbose_name_plural = 'التقييمات'
        unique_together = ('booking', 'client')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.rating} ⭐ من {self.client.get_full_name()}"


class Payment(models.Model):
    """Payment records"""
    PAYMENT_METHODS = (
        ('credit_card', 'بطاقة ائتمان'),
        ('debit_card', 'بطاقة خصم'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'تحويل بنكي'),
        ('cash', 'نقدي'),
    )
    
    PAYMENT_STATUSES = (
        ('pending', 'قيد الانتظار'),
        ('completed', 'مكتملة'),
        ('failed', 'فاشلة'),
        ('refunded', 'مسترجعة'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, unique=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'الدفع'
        verbose_name_plural = 'الدفعات'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.amount} درهم - {self.booking} - {self.get_status_display()}"
