from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
import logging
import json
import requests
import os
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from .models import CustomUser
from clients.models import ClientProfile

logger = logging.getLogger(__name__)

# Google OAuth Configuration - Load from environment variables
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/auth/google/callback/')


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


def google_login(request):
    """Redirect to Google OAuth for login/signup"""
    import secrets
    
    # Generate state to prevent CSRF
    state = secrets.token_urlsafe(32)
    request.session['google_oauth_state'] = state
    
    # Build Google OAuth URL
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'offline'
    }
    
    from urllib.parse import urlencode
    google_auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return redirect(google_auth_url)


def google_callback(request):
    """Handle Google OAuth callback after user authorizes"""
    code = request.GET.get('code')
    state = request.GET.get('state')
    error = request.GET.get('error')
    
    logger.info(f"Google callback received - code: {bool(code)}, state: {bool(state)}, error: {error}")
    
    # Check for errors
    if error:
        logger.error(f"Google OAuth error: {error}")
        messages.error(request, f'خطأ من Google: {error}')
        return redirect('signup')
    
    # Verify state token
    session_state = request.session.get('google_oauth_state')
    if not state or state != session_state:
        logger.error("State token mismatch in Google OAuth")
        messages.error(request, 'خطأ أمني: عدم تطابق الدولة')
        return redirect('signup')
    
    if not code:
        messages.error(request, 'لم يتم الحصول على رمز التفويض من Google')
        return redirect('signup')
    
    try:
        # Exchange code for access token
        token_data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        logger.info(f"Exchanging Google auth code for token at {GOOGLE_TOKEN_URL}")
        token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        logger.info(f"Token response status: {token_response.status_code}")
        token_response.raise_for_status()
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        
        if not access_token:
            messages.error(request, 'فشل الحصول على رمز الوصول')
            return redirect('signup')
        
        # Get user info from Google
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()
        
        email = user_info.get('email')
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        picture = user_info.get('picture', '')
        
        if not email:
            messages.error(request, 'لا يمكننا الحصول على بريدك الإلكتروني من Google')
            return redirect('signup')
        
        # Check if user exists
        try:
            user = CustomUser.objects.get(email=email)
            logger.info(f"Existing user found: {email}")
            # Update profile picture if available
            if picture and not user.profile_image:
                user.profile_image = picture
                user.save()
            login(request, user)
            messages.success(request, f'أهلا وسهلا {user.first_name}!')
            logger.info(f"User {email} logged in via Google OAuth")
            return redirect('home')
        except CustomUser.DoesNotExist:
            # Create new user from Google info
            logger.info(f"Creating new user: {email}")
            username = email.split('@')[0]
            # Ensure username is unique
            base_username = username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = CustomUser.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type='client',  # Default to client
                is_active=True
            )
            
            # Download and save profile picture if available
            if picture:
                try:
                    import tempfile
                    from django.core.files import File
                    from io import BytesIO
                    
                    img_response = requests.get(picture)
                    img_response.raise_for_status()
                    img_temp = tempfile.NamedTemporaryFile(delete=False)
                    img_temp.write(img_response.content)
                    img_temp.flush()
                    
                    with open(img_temp.name, 'rb') as f:
                        user.profile_image.save(f'{username}_profile.jpg', File(f), save=True)
                except Exception as e:
                    logger.warning(f"Could not save Google profile picture: {e}")
            
            # Set unusable password (OAuth users don't need passwords)
            user.set_unusable_password()
            user.save()
            
            # Create client profile
            try:
                ClientProfile.objects.create(user=user)
            except Exception as e:
                logger.warning(f"Could not create ClientProfile: {e}")
            
            login(request, user)
            messages.success(request, f'مرحبا {user.first_name}! تم إنشاء حسابك بنجاح')
            return redirect('home')
    
    except requests.RequestException as e:
        logger.error(f"Google OAuth request error: {e}")
        messages.error(request, 'فشل الاتصال بخادم Google')
        return redirect('signup')
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        messages.error(request, f'حدث خطأ في المصادقة: {str(e)}')
        return redirect('signup')

