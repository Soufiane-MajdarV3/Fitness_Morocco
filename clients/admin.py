from django.contrib import admin
from .models import ClientProfile, ClientProgress


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fitness_level', 'subscription_plan', 'age', 'weight')
    list_filter = ('fitness_level', 'subscription_plan')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ClientProgress)
class ClientProgressAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'weight')
    list_filter = ('date',)
    search_fields = ('client__user__first_name', 'client__user__last_name')
    ordering = ('-date',)
