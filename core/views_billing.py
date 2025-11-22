"""
Views for subscription pricing page and club/gym organization pages
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from payments.models import SubscriptionPlan, Organization
from trainers.models import Trainer
from bookings.models import Booking, Review
from decimal import Decimal


class SubscriptionPricingView(TemplateView):
    """Display subscription pricing page"""
    template_name = 'pricing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all active subscription plans
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('key')
        
        # Separate trainer and org plans
        trainer_plans = plans.filter(is_org_plan=False)
        org_plans = plans.filter(is_org_plan=True)
        
        # Current user's subscription if logged in
        user_subscription = None
        if self.request.user.is_authenticated:
            try:
                user_subscription = self.request.user.trainer_subscription
            except:
                pass
        
        context.update({
            'trainer_plans': trainer_plans,
            'org_plans': org_plans,
            'user_subscription': user_subscription,
            'page_title': 'اختر خطتك المناسبة - اختر Your Plan',
        })
        
        return context


class ClubListView(ListView):
    """Display all gyms/clubs/organizations"""
    model = Organization
    template_name = 'clubs_directory.html'
    context_object_name = 'clubs'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Organization.objects.filter(is_active=True).select_related('owner')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(city__icontains=search) |
                Q(description__icontains=search)
            )
        
        # City filter
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city=city)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get unique cities for filter
        cities = Organization.objects.filter(is_active=True).values_list('city', flat=True).distinct()
        cities = [c for c in cities if c]  # Remove empty cities
        
        context.update({
            'cities': sorted(cities),
            'search_query': self.request.GET.get('search', ''),
            'selected_city': self.request.GET.get('city', ''),
            'page_title': 'قائمة الأندية - Clubs Directory',
        })
        
        return context


class ClubDetailView(DetailView):
    """Display detailed club/gym page with trainers"""
    model = Organization
    template_name = 'club_detail.html'
    context_object_name = 'club'
    slug_field = 'id'
    slug_url_kwarg = 'club_id'
    
    def get_queryset(self):
        return Organization.objects.filter(is_active=True).select_related('subscription_plan')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.get_object()
        
        # Get trainers in this club via OrganizationInvitation acceptance
        club_trainers = club.trainer_subscriptions.filter(
            organization=club, trainer_subscription__is_active=True
        ).select_related(
            'trainer', 'trainer__trainer_profile'
        )
        
        # Get trainer profiles with ratings and reviews
        trainer_profiles = []
        for sub in club_trainers:
            try:
                profile = sub.trainer.trainer_profile
                # Get average rating and review count
                reviews = Review.objects.filter(trainer=profile)
                avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
                review_count = reviews.count()
                
                trainer_profiles.append({
                    'profile': profile,
                    'user': sub.trainer,
                    'subscription': sub,
                    'avg_rating': avg_rating,
                    'review_count': review_count,
                })
            except:
                continue
        
        # Get club reviews/ratings
        club_bookings = Booking.objects.filter(
            trainer__trainers__in=[p['profile'] for p in trainer_profiles],
            status='completed'
        )
        
        context.update({
            'trainers': trainer_profiles,
            'club_bookings_count': club_bookings.count(),
            'total_trainers': len(trainer_profiles),
            'page_title': f'{club.name} - نادي',
        })
        
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)


class ClubTrainerListView(ListView):
    """API endpoint to get trainers for a specific club"""
    model = Trainer
    
    def get_queryset(self):
        club_id = self.kwargs.get('club_id')
        club = get_object_or_404(Organization, id=club_id, is_active=True)
        
        # Get trainers linked to this club
        trainer_ids = club.trainer_subscriptions.filter(
            is_active=True
        ).values_list('trainer_id', flat=True)
        
        return Trainer.objects.filter(
            user_id__in=trainer_ids,
            is_approved=True
        ).select_related('user').prefetch_related('specialties')


# Pricing page view
def pricing_view(request):
    """Display subscription pricing and plans"""
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('key')
    
    user_subscription = None
    if request.user.is_authenticated:
        try:
            user_subscription = request.user.trainer_subscription
        except:
            pass
    
    context = {
        'trainer_plans': plans.filter(is_org_plan=False),
        'org_plans': plans.filter(is_org_plan=True),
        'user_subscription': user_subscription,
    }
    
    return render(request, 'pricing.html', context)


def clubs_directory_view(request):
    """Display clubs directory with search and filter"""
    clubs = Organization.objects.filter(is_active=True).select_related('owner')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        clubs = clubs.filter(
            Q(name__icontains=search) | 
            Q(city__icontains=search) |
            Q(description__icontains=search)
        )
    
    # City filter
    city = request.GET.get('city', '')
    if city:
        clubs = clubs.filter(city=city)
    
    # Get unique cities
    cities = Organization.objects.filter(is_active=True).values_list(
        'city', flat=True
    ).distinct().exclude(city='')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(clubs, 12)
    page_number = request.GET.get('page', 1)
    clubs_page = paginator.get_page(page_number)
    
    context = {
        'clubs': clubs_page,
        'cities': sorted(cities),
        'search_query': search,
        'selected_city': city,
    }
    
    return render(request, 'clubs_directory.html', context)


def club_detail_view(request, club_id):
    """Display detailed club/gym page"""
    club = get_object_or_404(Organization, id=club_id, is_active=True)
    
    # Get trainers in club
    from django.db import models
    club_trainers = club.trainer_subscriptions.filter(
        is_active=True
    ).select_related('trainer', 'trainer__trainer_profile')
    
    trainer_profiles = []
    for sub in club_trainers:
        try:
            profile = sub.trainer.trainer_profile
            reviews = Review.objects.filter(trainer=profile)
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
            
            trainer_profiles.append({
                'profile': profile,
                'user': sub.trainer,
                'avg_rating': avg_rating,
                'review_count': reviews.count(),
            })
        except:
            continue
    
    context = {
        'club': club,
        'trainers': trainer_profiles,
        'total_trainers': len(trainer_profiles),
    }
    
    return render(request, 'club_detail.html', context)


# Import models at end to avoid circular imports
from django.db import models
