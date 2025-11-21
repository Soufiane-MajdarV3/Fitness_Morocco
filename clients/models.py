from django.db import models
from django.contrib.auth import get_user_model
from trainers.models import SubscriptionPlan

User = get_user_model()


class ClientProfile(models.Model):
    """Extended client profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile',
                                limit_choices_to={'user_type': 'client'})
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True)
    fitness_level = models.CharField(max_length=20, choices=[
        ('beginner', 'مبتدئ'),
        ('intermediate', 'متوسط'),
        ('advanced', 'متقدم'),
    ], default='beginner')
    goals = models.TextField(blank=True)  # User's fitness goals
    weight = models.FloatField(null=True, blank=True)  # Current weight
    height = models.FloatField(null=True, blank=True)  # Height in cm
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'ملف العميل'
        verbose_name_plural = 'ملفات العملاء'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_fitness_level_display()}"
    
    def bmi(self):
        """Calculate BMI"""
        if self.weight and self.height:
            return (self.weight / (self.height / 100) ** 2)
        return None


class ClientProgress(models.Model):
    """Track client progress over time"""
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='progress_records')
    date = models.DateField(auto_now_add=True)
    weight = models.FloatField()
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'تقدم العميل'
        verbose_name_plural = 'تقدم العملاء'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.date}"
