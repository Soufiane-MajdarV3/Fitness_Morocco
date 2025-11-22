from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
import logging
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from .models import CustomUser
from clients.models import ClientProfile

logger = logging.getLogger(__name__)


class RegisterView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Handle cities - don't break if City model isn't available
        try:
            from trainers.models import City
            context['cities'] = City.objects.all()
        except Exception as e:
            logger.warning(f"Could not load City objects: {e}")
            context['cities'] = []
        return context
    
    def form_valid(self, form):
        try:
            user = form.save(commit=True)
            
            # Create client profile if registering as client
            if user.user_type == 'client':
                try:
                    ClientProfile.objects.create(user=user)
                except Exception as e:
                    logger.warning(f"Could not create ClientProfile: {e}")
            
            # Log successful registration
            logger.info(f"User {user.username} registered successfully as {user.user_type}")
            messages.success(self.request, f'تم إنشاء الحساب بنجاح! الرجاء تسجيل الدخول.')
            
            return redirect(self.success_url)
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            form.add_error(None, f'حدث خطأ أثناء إنشاء الحساب: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        logger.warning(f"Form submission failed with errors: {form.errors}")
        return super().form_invalid(form)


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username or email
            user = authenticate(request, username=username, password=password)
            if not user:
                # Try email
                try:
                    user_obj = CustomUser.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    pass
            
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'بيانات الدخول غير صحيحة')
    else:
        form = UserLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def profile_update_view(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    return render(request, 'profile_edit.html', {'form': form})
