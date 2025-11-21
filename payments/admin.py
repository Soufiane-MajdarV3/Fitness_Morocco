from django.contrib import admin
from .models import PaymentGatewayConfig


@admin.register(PaymentGatewayConfig)
class PaymentGatewayConfigAdmin(admin.ModelAdmin):
    list_display = ('gateway_name', 'is_active', 'created_at')
    list_filter = ('gateway_name', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
