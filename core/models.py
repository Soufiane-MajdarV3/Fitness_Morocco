from django.db import models


class SiteConfig(models.Model):
    """Global site configuration"""
    site_name = models.CharField(max_length=200, default='منصة فيتنس المغرب')
    tagline = models.CharField(max_length=500, blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    about_us = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    commission_percentage = models.FloatField(default=10)  # Platform commission
    
    class Meta:
        verbose_name = 'إعدادات الموقع'
        verbose_name_plural = 'إعدادات الموقع'
    
    def __str__(self):
        return self.site_name


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'رسالة التواصل'
        verbose_name_plural = 'رسائل التواصل'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"
