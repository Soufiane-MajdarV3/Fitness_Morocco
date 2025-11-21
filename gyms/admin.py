from django.contrib import admin
from .models import Gym, GymMembership


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'owner', 'rating', 'is_verified')
    list_filter = ('city', 'is_verified', 'created_at')
    search_fields = ('name', 'owner__first_name', 'owner__last_name', 'address')
    filter_horizontal = ('facilities',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GymMembership)
class GymMembershipAdmin(admin.ModelAdmin):
    list_display = ('gym', 'member', 'membership_type', 'start_date', 'end_date', 'is_active')
    list_filter = ('membership_type', 'is_active', 'start_date')
    search_fields = ('gym__name', 'member__first_name', 'member__last_name')
    readonly_fields = ('start_date',)
