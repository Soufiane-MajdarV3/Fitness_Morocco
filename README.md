# منصة فيتنس المغرب - Django Full Stack Project

**Fitness Morocco Coach & Gym Booking Platform**

A complete Django web application for connecting personal trainers and gyms in Morocco with clients for fitness sessions.

## 🚀 Project Features

- ✅ **User Authentication**: Client, Trainer, and Admin roles
- ✅ **Trainer Profiles**: Specialties, certificates, experience, ratings
- ✅ **Advanced Booking System**: Multi-step booking with payment
- ✅ **Dashboard**: Separate dashboards for clients and trainers
- ✅ **Review & Rating System**: Clients can rate trainers
- ✅ **Progress Tracking**: Clients can track their fitness progress
- ✅ **Search & Filters**: Find trainers by location, specialty, price, experience
- ✅ **Admin Panel**: Full Django admin for CRUD operations
- ✅ **RTL (Arabic) Support**: Full Arabic interface

## 📁 Project Structure

```
fitness_morocco/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # SQLite database
├── static/                        # Static files (CSS, JS, images)
├── media/                         # User uploads (profiles, documents)
├── templates/                     # HTML templates (shared)
│
├── fitness_morocco/               # Main project settings
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI application
│   └── asgi.py                   # ASGI application
│
├── authentication/                # User authentication app
│   ├── models.py                 # CustomUser model
│   ├── views.py                  # Auth views (login, signup, profile)
│   ├── forms.py                  # Auth forms
│   ├── admin.py                  # Admin configuration
│   └── urls.py                   # Auth URLs
│
├── core/                          # Core app (homepage, trainers list)
│   ├── models.py                 # SiteConfig, ContactMessage
│   ├── views.py                  # HomeView, TrainerListView, TrainerDetailView
│   ├── admin.py                  # Admin configuration
│   └── management/commands/
│       └── seed_data.py          # Data seeding command
│
├── trainers/                      # Trainer management
│   ├── models.py                 # Trainer, City, SessionType, Certificate, etc.
│   ├── views.py                  # Trainer views
│   ├── forms.py                  # Trainer forms
│   └── admin.py                  # Admin configuration
│
├── clients/                       # Client management
│   ├── models.py                 # ClientProfile, ClientProgress
│   ├── views.py                  # Client views
│   ├── forms.py                  # Client forms
│   └── admin.py                  # Admin configuration
│
├── bookings/                      # Booking system
│   ├── models.py                 # Booking, Review, Payment
│   ├── views.py                  # Booking views
│   ├── forms.py                  # Booking forms
│   └── admin.py                  # Admin configuration
│
├── dashboard/                     # User dashboards
│   ├── views.py                  # Dashboard views (client & trainer)
│   ├── models.py                 # DashboardCache
│   └── admin.py                  # Admin configuration
│
├── gyms/                          # Gym management
│   ├── models.py                 # Gym, GymMembership
│   ├── admin.py                  # Admin configuration
│   └── views.py                  # Gym views
│
└── payments/                      # Payment integration
    ├── models.py                 # PaymentGatewayConfig
    └── admin.py                  # Admin configuration
```

## 🗄️ Database Models

### Authentication
- **CustomUser**: Extended Django User with user_type (client/trainer/admin), profile image, bio

### Trainers
- **Trainer**: Trainer profile with specialties, experience, price, rating
- **TrainerAvailability**: Weekly availability slots
- **City**: Cities in Morocco
- **SessionType**: Types of training sessions
- **Certificate**: Trainer qualifications
- **SubscriptionPlan**: Gold/Platinum/Diamond plans

### Clients
- **ClientProfile**: Extended client info (age, fitness level, weight, height)
- **ClientProgress**: Track client progress over time

### Bookings
- **Booking**: Session reservation with status (pending/confirmed/completed/cancelled)
- **Review**: Client ratings and reviews of trainers
- **Payment**: Payment records for bookings

### Gyms
- **Gym**: Gym/fitness center profile
- **GymMembership**: Gym membership records

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Step 1: Clone/Navigate to Project
```bash
cd /home/sofiane/Desktop/SaaS/Fitness
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations
```bash
python3 manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python3 manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 6: Seed Initial Data (Optional)
```bash
python3 manage.py seed_data
# Creates cities, session types, 5 sample trainers, 20 sample clients, bookings, and reviews
```

### Step 7: Run Development Server
```bash
python3 manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### Step 8: Access Admin Panel
Visit `http://localhost:8000/admin` and login with superuser credentials.

## 📱 Key URLs

| URL | Purpose | Requires Auth |
|-----|---------|---------------|
| `/` | Homepage | No |
| `/login/` | User login | No |
| `/signup/` | User registration | No |
| `/trainers/` | Trainer listing | No |
| `/trainer/<id>/` | Trainer profile | No |
| `/booking/<trainer_id>/` | Book a session | Yes |
| `/dashboard/` | Client dashboard | Yes (Client) |
| `/trainer-dashboard/` | Trainer dashboard | Yes (Trainer) |
| `/bookings/` | Bookings list | Yes |
| `/profile/` | User profile | Yes |
| `/admin/` | Admin panel | Yes (Admin) |

## 👥 User Roles

### Client
- Browse trainers
- Book sessions
- View bookings history
- Track progress
- Rate trainers
- View dashboard with statistics

### Trainer
- Manage profile & certificates
- Set availability
- View bookings
- Track earnings
- See client reviews
- View trainer dashboard

### Admin
- Manage all users
- Approve/reject trainers
- Manage bookings
- Handle payments
- View system analytics
- Configure site settings

## 🔐 Authentication Flow

1. **Registration**: New users select role (client/trainer)
2. **Login**: Email/username + password authentication
3. **Profile Setup**: Complete profile information
4. **Verification**: Trainer verification by admin
5. **Dashboard**: Access role-specific dashboard

## 💰 Booking Flow

1. **Browse**: Client searches trainers with filters
2. **Select**: Client views trainer profile
3. **Book**: Fill booking form with date/time/duration
4. **Payment**: Select payment method
5. **Confirmation**: Booking confirmed
6. **Complete**: After session, leave review

## 📊 Available Filters

- **Location (City)**: Filter by city
- **Specialty**: Filter by training type
- **Price Range**: Min/Max hourly rate
- **Experience**: Minimum years of experience
- **Rating**: Minimum rating stars
- **Sort**: By rating, price, experience, newest

## 🎨 Frontend Integration

### Existing HTML Templates
Place your HTML files in `templates/` directory:
```
templates/
├── base.html                 # Base template with navbar/footer
├── navbar.html              # Navigation partial
├── footer.html              # Footer partial
├── index.html               # Homepage
├── trainers.html            # Trainer listing
├── trainer_detail.html      # Trainer profile
├── booking.html             # Booking form
├── dashboard.html           # Client dashboard
├── trainer_dashboard.html   # Trainer dashboard
├── registration/
│   ├── login.html          # Login form
│   └── signup.html         # Registration form
└── ... (other templates)
```

### Using Django Template Tags
```django
<!-- Static files -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- URL reversing -->
<a href="{% url 'home' %}">Home</a>
<a href="{% url 'trainer_detail' trainer.id %}">View Trainer</a>

<!-- Conditional content -->
{% if user.is_authenticated %}
    <a href="{% url 'client_dashboard' %}">Dashboard</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}

<!-- Loops -->
{% for trainer in trainers %}
    <div class="trainer-card">
        <h3>{{ trainer.user.get_full_name }}</h3>
        <p>{{ trainer.bio }}</p>
    </div>
{% endfor %}

<!-- Include partials -->
{% include 'navbar.html' %}
{% include 'footer.html' %}
```

## 🎨 Tailwind CSS & Bootstrap

### Option 1: Use CDN (Already in templates)
```html
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
```

### Option 2: NPM Installation
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Configure `tailwind.config.js`:
```javascript
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Build CSS:
```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

## 📝 Common Tasks

### Create a New Trainer
1. Signup as trainer
2. Complete profile
3. Admin approves trainer
4. Set availability
5. Upload certificates

### Book a Session
1. Login as client
2. Browse trainers
3. Click "Book Session"
4. Fill booking form
5. Select payment method
6. Confirm booking

### Add Review
1. Complete booking (session date passes)
2. Go to bookings list
3. Click "Add Review"
4. Rate and comment
5. Submit

### Filter Trainers
Visit `/trainers/` and use:
```
?city=الدار%20البيضاء&specialty=1&min_price=100&max_price=300&sort=-rating
```

## 🔍 Admin Features

### User Management
- View all users by type
- Approve trainer applications
- Suspend/deactivate accounts

### Trainer Management
- View trainer profiles
- Approve certificates
- Manage specialties
- Update ratings

### Booking Management
- View all bookings
- Change booking status
- View payment records

### Site Configuration
- Set commission percentage
- Manage contact messages
- Configure payment gateways

## 🚀 Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS` in settings.py
- [ ] Use environment variables for secrets
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure email backend
- [ ] Set up static files collection
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure payment gateway
- [ ] Set up regular backups
- [ ] Configure CDN for media files
- [ ] Set up monitoring/alerts

## 📱 API Endpoints (for future mobile app)

```
GET    /api/trainers/              # List trainers
GET    /api/trainers/<id>/         # Get trainer details
GET    /api/trainers/<id>/reviews/ # Get trainer reviews
POST   /api/bookings/              # Create booking
GET    /api/bookings/              # List user bookings
POST   /api/bookings/<id>/review/  # Add review
```

## 🐛 Troubleshooting

### Issue: "No module named 'authentication'"
**Solution**: Ensure all apps are in INSTALLED_APPS in settings.py

### Issue: "Relation does not exist"
**Solution**: Run migrations: `python3 manage.py migrate`

### Issue: Static files not loading
**Solution**: 
```bash
python3 manage.py collectstatic --noinput
```

### Issue: "User has no trainer profile"
**Solution**: Navigate to `/trainer-dashboard/` which auto-creates profile

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/)
- [Bootstrap Docs](https://getbootstrap.com/)
- [Font Awesome Icons](https://fontawesome.com/)

## 📞 Support

For issues or questions:
1. Check the Django error message carefully
2. Review the model definitions
3. Check URL patterns match
4. Verify user authentication/permissions

## 📄 License

This project is for educational purposes.

---

**Happy Coding! 🎉**
