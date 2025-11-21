# Fitness Morocco - Complete Django Project

## 🎯 Project Overview

Fitness Morocco is a comprehensive Django-based platform for booking personal trainers and fitness sessions. The project has been fully converted from raw HTML templates to production-ready Django templates with complete backend integration.

**Status:** ✅ **COMPLETE & TESTED**

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API/Views](#apiviews)
7. [Templates](#templates)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment

### Installation

```bash
# Navigate to project directory
cd /home/sofiane/Desktop/SaaS/Fitness

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Load seed data (optional but recommended)
python3 manage.py seed_data

# Start development server
python3 manage.py runserver
```

### Access the Application

- **Homepage:** http://127.0.0.1:8000/
- **Trainers List:** http://127.0.0.1:8000/trainers/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Login:** http://127.0.0.1:8000/login/
- **Register:** http://127.0.0.1:8000/signup/

---

## 📁 Project Structure

```
fitness_morocco/
│
├── manage.py                           # Django management script
├── db.sqlite3                          # SQLite database
├── requirements.txt                    # Python dependencies
│
├── fitness_morocco/                    # Project configuration
│   ├── settings.py                     # Django settings
│   ├── urls.py                         # URL routing (25+ patterns)
│   ├── wsgi.py                         # WSGI application
│   └── asgi.py                         # ASGI application
│
├── templates/                          # HTML templates (17 files)
│   ├── base.html                       # Master template
│   ├── navbar.html                     # Navigation
│   ├── footer.html                     # Footer
│   ├── index.html                      # Homepage
│   ├── trainers.html                   # Trainer listing
│   ├── trainer_detail.html             # Trainer profile
│   ├── booking.html                    # Booking form
│   ├── booking_confirmation.html       # Payment selection
│   ├── booking_success.html            # Confirmation
│   ├── bookings_list.html              # Booking history
│   ├── add_review.html                 # Review form
│   ├── profile.html                    # User profile
│   ├── profile_edit.html               # Edit profile
│   ├── dashboard.html                  # Client dashboard
│   ├── trainer-dashboard.html          # Trainer dashboard
│   └── registration/
│       ├── login.html                  # Login page
│       └── signup.html                 # Registration page
│
├── media/                              # User-uploaded files (profile images)
├── static/                             # Static assets (CSS, JS, images)
│
├── core/                               # Core app
│   ├── models.py                       # SiteConfig, ContactMessage
│   ├── views.py                        # HomeView, TrainerListView, TrainerDetailView
│   ├── admin.py                        # Admin configuration
│   └── management/commands/
│       └── seed_data.py                # Seed database with test data
│
├── authentication/                     # Authentication app
│   ├── models.py                       # CustomUser model
│   ├── views.py                        # Auth views (login, signup, profile)
│   ├── forms.py                        # Auth forms (3)
│   └── admin.py                        # Admin configuration
│
├── trainers/                           # Trainers app
│   ├── models.py                       # 6 models (Trainer, Availability, etc.)
│   ├── views.py                        # Trainer-related views
│   ├── forms.py                        # Trainer forms (3)
│   └── admin.py                        # Admin configuration
│
├── clients/                            # Clients app
│   ├── models.py                       # 2 models (ClientProfile, Progress)
│   ├── views.py                        # Client-related views
│   ├── forms.py                        # Client forms
│   └── admin.py                        # Admin configuration
│
├── bookings/                           # Bookings app
│   ├── models.py                       # 3 models (Booking, Review, Payment)
│   ├── views.py                        # 6 booking-related functions
│   ├── forms.py                        # 3 forms (Booking, Review, Payment)
│   └── admin.py                        # Admin configuration
│
├── dashboard/                          # Dashboard app
│   ├── models.py                       # DashboardCache model
│   ├── views.py                        # Dashboard views
│   └── admin.py                        # Admin configuration
│
├── gyms/                               # Gyms app
│   ├── models.py                       # Gym models
│   └── admin.py                        # Admin configuration
│
└── payments/                           # Payments app
    ├── models.py                       # Payment configuration
    └── admin.py                        # Admin configuration
```

---

## ✨ Features

### 1. User Authentication & Profiles
- ✅ User registration (Client/Trainer roles)
- ✅ Login/Logout functionality
- ✅ Profile management
- ✅ Profile image upload
- ✅ Account verification system
- ✅ Role-based access control

### 2. Trainer Management
- ✅ Trainer profiles with ratings
- ✅ Certifications & credentials display
- ✅ Experience years tracking
- ✅ Session type specialties
- ✅ Availability scheduling
- ✅ Price per hour setting
- ✅ Total sessions counter

### 3. Search & Filtering
- ✅ Filter trainers by city
- ✅ Filter by specialty (session type)
- ✅ Price range filtering
- ✅ Experience level filtering
- ✅ Sort by rating/price/experience
- ✅ Real-time search

### 4. Booking System
- ✅ Multi-step booking process
- ✅ Date/time selection
- ✅ Duration options (30min to 8hrs)
- ✅ Automatic price calculation
- ✅ Payment method selection (Card, Wallet, Bank)
- ✅ Booking confirmation
- ✅ Booking cancellation
- ✅ Booking history with filters

### 5. Reviews & Ratings
- ✅ 5-star rating system
- ✅ Written reviews/comments
- ✅ Helpful features checkboxes
- ✅ Trainer average rating calculation
- ✅ Review display on trainer profiles

### 6. Dashboards
- **Client Dashboard:**
  - Upcoming bookings
  - Completed sessions
  - Booking statistics
  - Quick actions (book, profile, history)
  
- **Trainer Dashboard:**
  - Upcoming sessions
  - Pending confirmations
  - Completed sessions with reviews
  - Monthly earnings
  - Client management
  - Session statistics

### 7. Design & UX
- ✅ Responsive design (mobile-first)
- ✅ RTL (Arabic) layout support
- ✅ Tailwind CSS styling
- ✅ Font Awesome icons
- ✅ Dark mode support
- ✅ Form validation
- ✅ Error messages
- ✅ Success notifications

---

## 🔧 Installation Guide

### 1. System Requirements
```bash
Python 3.8+ installed
Git (for version control)
pip (Python package manager)
```

### 2. Clone/Navigate to Project
```bash
cd /home/sofiane/Desktop/SaaS/Fitness
```

### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Setup
```bash
# Run migrations
python3 manage.py migrate

# Create superuser (for admin)
python3 manage.py createsuperuser

# OR load seed data
python3 manage.py seed_data
```

### 6. Collect Static Files (Production)
```bash
python3 manage.py collectstatic
```

### 7. Run Development Server
```bash
python3 manage.py runserver
# Server runs at http://127.0.0.1:8000/
```

---

## 📖 Usage

### For Clients

1. **Register Account**
   - Go to `/signup/`
   - Enter details (name, email, password)
   - Select role: "Client"
   - Submit

2. **Browse Trainers**
   - Visit `/trainers/`
   - Use filters (city, specialty, price, experience)
   - Click trainer card to view profile

3. **View Trainer Profile**
   - See trainer details, ratings, certifications
   - View reviews from other clients
   - Check availability

4. **Book a Session**
   - Click "احجز جلسة الآن" button
   - Select session type
   - Choose date & time
   - Set duration
   - Add notes (optional)
   - Review price
   - Proceed to payment

5. **Manage Bookings**
   - Visit `/bookings/`
   - View upcoming sessions
   - Cancel bookings (if allowed)
   - Leave reviews after completion
   - View booking history

6. **Update Profile**
   - Go to `/profile/`
   - Click "تعديل الملف الشخصي"
   - Update information
   - Upload profile picture
   - Save changes

### For Trainers

1. **Register as Trainer**
   - Go to `/signup/`
   - Select role: "Trainer"
   - Fill trainer-specific details

2. **Manage Profile**
   - Update qualifications & certifications
   - Set hourly rate
   - Upload profile picture
   - Add bio/specialties

3. **View Dashboard**
   - Access `/trainer-dashboard/`
   - See upcoming sessions
   - Review pending bookings
   - Track earnings
   - View client feedback

4. **Manage Availability**
   - Set working hours
   - Mark unavailable dates
   - Update session types offered

### For Admins

1. **Access Admin Panel**
   - Go to `/admin/`
   - Login with superuser credentials

2. **Manage Users**
   - View/edit/delete users
   - Approve trainers
   - Manage user roles

3. **Manage Trainers**
   - View trainer profiles
   - Approve/reject trainers
   - Manage certifications
   - Monitor ratings

4. **View Bookings**
   - See all bookings
   - Filter by status
   - Handle disputes
   - Process refunds

5. **Analytics**
   - View platform statistics
   - Monitor bookings
   - Track revenue

---

## 🛣️ API/Views

### URLs & Views

#### Public Pages
| URL | View | Template |
|-----|------|----------|
| `/` | HomeView | index.html |
| `/trainers/` | TrainerListView | trainers.html |
| `/trainer/<id>/` | TrainerDetailView | trainer_detail.html |

#### Authentication
| URL | View | Template |
|-----|------|----------|
| `/signup/` | RegisterView | registration/signup.html |
| `/login/` | login_view | registration/login.html |
| `/logout/` | logout_view | — |
| `/profile/` | profile_view | profile.html |
| `/profile/edit/` | profile_update_view | profile_edit.html |

#### Bookings
| URL | View | Template |
|-----|------|----------|
| `/booking/<id>/` | booking_view | booking.html |
| `/booking/<id>/confirmation/` | booking_confirmation_view | booking_confirmation.html |
| `/booking/<id>/success/` | booking_success_view | booking_success.html |
| `/bookings/` | booking_list_view | bookings_list.html |
| `/booking/<id>/review/` | add_review_view | add_review.html |

#### Dashboards
| URL | View | Template |
|-----|------|----------|
| `/dashboard/` | client_dashboard_view | dashboard.html |
| `/trainer-dashboard/` | trainer_dashboard_view | trainer-dashboard.html |

---

## 📝 Templates

### Template Hierarchy

```
base.html (Master)
├── navbar.html (included)
├── footer.html (included)
└── [Child templates extend base.html]
    ├── index.html
    ├── trainers.html
    ├── trainer_detail.html
    ├── booking.html
    ├── booking_confirmation.html
    ├── booking_success.html
    ├── bookings_list.html
    ├── add_review.html
    ├── profile.html
    ├── profile_edit.html
    ├── dashboard.html
    ├── trainer-dashboard.html
    ├── registration/login.html
    └── registration/signup.html
```

### Template Features

All templates include:
- ✅ RTL (Arabic) support
- ✅ Responsive design
- ✅ CSRF protection on forms
- ✅ Form error display
- ✅ User authentication checks
- ✅ Dynamic context variables
- ✅ Tailwind CSS styling
- ✅ Font Awesome icons

---

## 🐛 Troubleshooting

### Issue: Server won't start

**Solution:**
```bash
# Check for syntax errors
python3 manage.py check

# Run migrations
python3 manage.py migrate

# Check port availability (8000 might be in use)
python3 manage.py runserver 8001
```

### Issue: Database errors

**Solution:**
```bash
# Reset database (development only)
rm db.sqlite3
python3 manage.py migrate
python3 manage.py seed_data
```

### Issue: Missing static files

**Solution:**
```bash
python3 manage.py collectstatic --noinput
```

### Issue: User can't login

**Solution:**
1. Check user exists in admin panel
2. Verify password is correct
3. Ensure user account is active
4. Check user role/permissions

### Issue: Images not uploading

**Solution:**
1. Check MEDIA_ROOT and MEDIA_URL in settings
2. Verify write permissions on media directory
3. Check file size limit
4. Ensure correct file type

### Issue: Template not found error

**Solution:**
```bash
# Check TEMPLATES setting in settings.py
# Verify template file exists
# Restart development server
```

---

## 📞 Support & Contact

For questions or issues:
- Check documentation files in project root
- Review Django error messages carefully
- Use Django admin for data management
- Check terminal output for detailed errors

---

## 📄 Additional Documentation

- `README.md` - Project overview
- `TEMPLATES_CONVERSION_SUMMARY.md` - Template conversion details
- `INTEGRATION_GUIDE.md` - Integration instructions
- `COMMANDS.md` - Available management commands
- `PROJECT_SUMMARY.md` - Complete project summary
- `FILE_INVENTORY.md` - File and model inventory

---

## ✅ Checklist for Deployment

- [ ] Update `DEBUG = False` in settings.py
- [ ] Set `ALLOWED_HOSTS` in settings.py
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up static file serving (Nginx/Whitenoise)
- [ ] Configure email backend
- [ ] Set up SSL/TLS certificates
- [ ] Configure domain name
- [ ] Set environment variables
- [ ] Run security checks: `python3 manage.py check --deploy`
- [ ] Create superuser for production
- [ ] Set up backups
- [ ] Configure logging
- [ ] Set up monitoring

---

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Template Language](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Font Awesome Icons](https://fontawesome.com/docs)

---

**Last Updated:** November 21, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
