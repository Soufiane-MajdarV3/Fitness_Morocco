from django.db import models

# Payments are already handled in bookings.models.Payment
# This app is for additional payment gateway integration in the future
# Such as Stripe, PayPal, etc.

class PaymentGatewayConfig(models.Model):
    """Configuration for payment gateways"""
    GATEWAY_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('local', 'Local Payment'),
    )
    
    gateway_name = models.CharField(max_length=50, choices=GATEWAY_CHOICES)
    api_key = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'إعدادات بوابة الدفع'
        verbose_name_plural = 'إعدادات بوابات الدفع'
    
    def __str__(self):
        return f"{self.get_gateway_name_display()} - {'Active' if self.is_active else 'Inactive'}"
