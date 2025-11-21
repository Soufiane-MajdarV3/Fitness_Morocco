from django.db import models

# Dashboard views and analytics are computed from other models
# This app handles dashboard views and potentially stores cached analytics

class DashboardCache(models.Model):
    """Cache for dashboard statistics to improve performance"""
    cache_key = models.CharField(max_length=200, unique=True)
    cache_value = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        verbose_name = 'ذاكرة التخزين المؤقت'
        verbose_name_plural = 'ذاكرات التخزين المؤقت'
    
    def __str__(self):
        return self.cache_key
