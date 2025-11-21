from django.contrib import admin
from .models import City, SessionType, Certificate, Trainer, TrainerAvailability, SubscriptionPlan


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(SessionType)
class SessionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer', 'issuer', 'issue_year', 'is_verified')
    list_filter = ('is_verified', 'issue_year')
    search_fields = ('name', 'trainer__user__first_name', 'trainer__user__last_name')
    ordering = ('-created_at',)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_years', 'price_per_hour', 'rating', 'is_approved', 'total_sessions')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('specialties',)
    ordering = ('-rating',)
    
    fieldsets = (
        ('معلومات المستخدم', {'fields': ('user',)}),
        ('معلومات المدرب', {'fields': ('specialties', 'experience_years', 'price_per_hour', 'bio')}),
        ('التقييمات', {'fields': ('rating', 'total_reviews', 'total_sessions', 'earnings')}),
        ('التحقق', {'fields': ('is_approved',)}),
    )


@admin.register(TrainerAvailability)
class TrainerAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
    search_fields = ('trainer__user__first_name', 'trainer__user__last_name')


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'price_monthly', 'sessions_per_month')
    list_filter = ('plan_type',)
    search_fields = ('name',)
