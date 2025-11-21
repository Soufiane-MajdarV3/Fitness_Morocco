from django.db import models
from django.contrib.auth import get_user_model
from trainers.models import City, SessionType

User = get_user_model()


class Gym(models.Model):
    """Gym/fitness center profile"""
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gyms',
                              limit_choices_to={'user_type': 'admin'})
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='gyms/', null=True, blank=True)
    description = models.TextField(blank=True)
    equipment = models.JSONField(default=list)  # List of equipment available
    facilities = models.ManyToManyField(SessionType, related_name='gyms_offering')
    rating = models.FloatField(default=0.0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'نادي رياضي'
        verbose_name_plural = 'الأندية الرياضية'
    
    def __str__(self):
        return f"{self.name} - {self.city}"


class GymMembership(models.Model):
    """Gym membership records"""
    MEMBERSHIP_TYPES = (
        ('monthly', 'شهري'),
        ('quarterly', 'ربع سنوي'),
        ('annual', 'سنوي'),
    )
    
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gym_memberships',
                               limit_choices_to={'user_type': 'client'})
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'عضوية النادي'
        verbose_name_plural = 'عضويات النوادي'
    
    def __str__(self):
        return f"{self.member.get_full_name()} - {self.gym.name}"
