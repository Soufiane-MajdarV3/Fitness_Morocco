from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from trainers.models import City, SessionType, Trainer
from .models import ContactMessage


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()[:6]
        context['session_types'] = SessionType.objects.all()
        context['featured_trainers'] = Trainer.objects.filter(
            is_approved=True
        ).order_by('-rating')[:6]
        return context


class TrainerListView(ListView):
    model = Trainer
    template_name = 'trainers.html'
    context_object_name = 'trainers'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Trainer.objects.filter(is_approved=True).order_by('-rating')
        
        # Filter by city
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(user__city=city)
        
        # Filter by specialty
        specialty = self.request.GET.get('specialty')
        if specialty:
            queryset = queryset.filter(specialties__id=specialty)
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price_per_hour__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_hour__lte=max_price)
        
        # Filter by experience
        experience = self.request.GET.get('experience')
        if experience:
            queryset = queryset.filter(experience_years__gte=experience)
        
        # Filter by rating
        rating = self.request.GET.get('rating')
        if rating:
            queryset = queryset.filter(rating__gte=rating)
        
        # Sort
        sort_by = self.request.GET.get('sort', '-rating')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()
        context['session_types'] = SessionType.objects.all()
        return context


class TrainerDetailView(TemplateView):
    template_name = 'trainer_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainer_id = self.kwargs.get('trainer_id')
        try:
            context['trainer'] = Trainer.objects.get(id=trainer_id)
            context['reviews'] = context['trainer'].reviews.all()
            context['certificates'] = context['trainer'].user.certificates.all()
        except Trainer.DoesNotExist:
            context['trainer'] = None
        return context
