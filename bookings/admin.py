from django.contrib import admin
from .models import Booking, Review, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'trainer', 'booking_date', 'start_time', 'status', 'total_price')
    list_filter = ('status', 'booking_date', 'session_type')
    search_fields = ('client__first_name', 'client__last_name', 'trainer__user__first_name', 'trainer__user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('معلومات الحجز', {'fields': ('client', 'trainer', 'session_type')}),
        ('التفاصيل', {'fields': ('booking_date', 'start_time', 'duration_minutes', 'total_price')}),
        ('الحالة', {'fields': ('status', 'cancelled_by', 'cancelled_reason')}),
        ('إضافي', {'fields': ('notes', 'created_at', 'updated_at')}),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'trainer', 'client', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('trainer__user__first_name', 'client__first_name', 'comment')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'booking__client__first_name')
    readonly_fields = ('created_at', 'updated_at')
