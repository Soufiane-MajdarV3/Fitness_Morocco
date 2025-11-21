from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class City(models.Model):
    """Cities in Morocco"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'المدينة'
        verbose_name_plural = 'المدن'
    
    def __str__(self):
        return self.name


class SessionType(models.Model):
    """Types of training sessions"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Font Awesome icon class
    
    class Meta:
        verbose_name = 'نوع الجلسة'
        verbose_name_plural = 'أنواع الجلسات'
    
    def __str__(self):
        return self.name


class Certificate(models.Model):
    """Trainer certificates/qualifications"""
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates',
                                limit_choices_to={'user_type': 'trainer'})
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_year = models.IntegerField()
    document = models.FileField(upload_to='certificates/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'شهادة'
        verbose_name_plural = 'شهادات'
    
    def __str__(self):
        return f"{self.name} - {self.trainer.get_full_name()}"


class Trainer(models.Model):
    """Trainer profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile',
                                limit_choices_to={'user_type': 'trainer'})
    specialties = models.ManyToManyField(SessionType, related_name='trainers')
    experience_years = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    bio = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.IntegerField(default=0)
    total_sessions = models.IntegerField(default=0)
    earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'ملف المدرب'
        verbose_name_plural = 'ملفات المدربين'
        ordering = ['-rating']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.experience_years} سنوات"
    
    def average_rating(self):
        from bookings.models import Review
        reviews = Review.objects.filter(trainer=self)
        if not reviews.exists():
            return 0
        return sum(r.rating for r in reviews) / reviews.count()


class TrainerAvailability(models.Model):
    """Trainer time slots availability"""
    DAYS_OF_WEEK = (
        ('0', 'الاثنين'),
        ('1', 'الثلاثاء'),
        ('2', 'الأربعاء'),
        ('3', 'الخميس'),
        ('4', 'الجمعة'),
        ('5', 'السبت'),
        ('6', 'الأحد'),
    )
    
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.CharField(max_length=1, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        verbose_name = 'توفر المدرب'
        verbose_name_plural = 'توفرات المدربين'
        unique_together = ('trainer', 'day_of_week', 'start_time', 'end_time')
    
    def __str__(self):
        return f"{self.trainer.user.get_full_name()} - {self.get_day_of_week_display()}"


class SubscriptionPlan(models.Model):
    """Subscription plans for trainers/clients"""
    PLAN_TYPES = (
        ('gold', 'ذهبي'),
        ('platinum', 'بلاتيني'),
        ('diamond', 'ماسي'),
    )
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    price_monthly = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    sessions_per_month = models.IntegerField(null=True, blank=True)
    features = models.JSONField(default=list)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'خطة الاشتراك'
        verbose_name_plural = 'خطط الاشتراك'
    
    def __str__(self):
        return f"{self.name} - {self.price_monthly} درهم"
