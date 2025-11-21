"""
URL configuration for FITMO (Fitness Morocco) project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Core views
from core.views import HomeView, TrainerListView, TrainerDetailView, contact_view, client_progress

# Authentication views
from authentication.views import RegisterView, login_view, logout_view, profile_view, profile_update_view

# Bookings views
from bookings.views import (
    booking_view, booking_confirmation_view, booking_success_view,
    booking_list_view, add_review_view
)

# Dashboard views
from dashboard.views import client_dashboard_view, trainer_dashboard_view

# Trainer views
from trainers.views import (
    trainer_edit_profile, trainer_availability, delete_availability,
    trainer_my_clients, trainer_earnings, trainer_bookings, update_booking_status
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core URLs
    path('', HomeView.as_view(), name='home'),
    path('trainers/', TrainerListView.as_view(), name='trainers'),
    path('trainer/<int:trainer_id>/', TrainerDetailView.as_view(), name='trainer_detail'),
    path('contact/', contact_view, name='contact'),
    
    # Authentication URLs
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_update_view, name='profile_edit'),
    
    # Bookings URLs
    path('booking/<int:trainer_id>/', booking_view, name='booking'),
    path('booking/<int:booking_id>/confirmation/', booking_confirmation_view, name='booking_confirmation'),
    path('booking/<int:booking_id>/success/', booking_success_view, name='booking_success'),
    path('bookings/', booking_list_view, name='booking_list'),
    path('booking/<int:booking_id>/review/', add_review_view, name='add_review'),
    
    # Dashboard URLs
    path('dashboard/', client_dashboard_view, name='client_dashboard'),
    path('trainer-dashboard/', trainer_dashboard_view, name='trainer_dashboard'),
    path('progress/', client_progress, name='client_progress'),
    
    # Trainer URLs
    path('trainer/edit-profile/', trainer_edit_profile, name='trainer_edit_profile'),
    path('trainer/availability/', trainer_availability, name='trainer_availability'),
    path('trainer/availability/<int:availability_id>/delete/', delete_availability, name='delete_availability'),
    path('trainer/my-clients/', trainer_my_clients, name='trainer_my_clients'),
    path('trainer/earnings/', trainer_earnings, name='trainer_earnings'),
    path('trainer/bookings/', trainer_bookings, name='trainer_bookings'),
    path('trainer/booking/<int:booking_id>/status/', update_booking_status, name='update_booking_status'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
