from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from trainers.models import City, SessionType, Trainer, SubscriptionPlan
from .models import ContactMessage
from clients.models import ClientProgress, ClientProfile
from django.contrib import messages


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
        
        # Filter by city (by name or code)
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(user__city__icontains=city)
        
        # Filter by specialty
        specialty = self.request.GET.get('specialty')
        if specialty:
            queryset = queryset.filter(specialties__id=specialty).distinct()
        
        # Filter by price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            try:
                queryset = queryset.filter(price_per_hour__gte=float(min_price))
            except (ValueError, TypeError):
                pass
                
        if max_price:
            try:
                queryset = queryset.filter(price_per_hour__lte=float(max_price))
            except (ValueError, TypeError):
                pass
        
        # Sort
        sort_by = self.request.GET.get('sort', '-rating')
        if sort_by in ['-rating', 'price_per_hour', '-price_per_hour', '-experience_years']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-rating')
        
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


def contact_view(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                user=request.user if request.user.is_authenticated else None
            )
            messages.success(request, 'شكراً لرسالتك. سنتواصل معك قريباً.')
            return redirect('contact')
        else:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
    
    return render(request, 'contact.html')


@login_required
def client_progress(request):
    """View and track client progress"""
    if request.user.user_type != 'client':
        return render(request, 'error.html', {'message': 'Access denied'})
    
    try:
        client_profile = ClientProfile.objects.get(user=request.user)
    except ClientProfile.DoesNotExist:
        client_profile = ClientProfile.objects.create(user=request.user)
    
    # Get progress records
    progress_records = ClientProgress.objects.filter(client=client_profile).order_by('-date')
    
    # Handle adding new progress
    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        notes = request.POST.get('notes')
        
        if weight or height or notes:
            ClientProgress.objects.create(
                client=client_profile,
                weight=float(weight) if weight else None,
                height=float(height) if height else None,
                notes=notes
            )
            messages.success(request, 'تم تسجيل التقدم بنجاح!')
            return redirect('client_progress')
    
    # Calculate progress statistics
    latest = progress_records.first()
    oldest = progress_records.last()
    
    weight_change = None
    if latest and oldest and latest.weight and oldest.weight:
        weight_change = latest.weight - oldest.weight
    
    return render(request, 'client_progress.html', {
        'client_profile': client_profile,
        'progress_records': progress_records,
        'latest': latest,
        'oldest': oldest,
        'weight_change': weight_change,
    })
