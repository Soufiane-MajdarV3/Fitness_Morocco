# Frontend Integration Guide - Subscription & Club Pages

## Overview

This guide documents the complete frontend integration for the subscription billing system and club discovery pages. All pages are fully integrated with the Django backend and styled with Tailwind CSS with Arabic (RTL) support.

## Pages Implemented

### 1. **Pricing Page** (`/pricing/`)
- **File**: `templates/pricing.html`
- **View**: `core.views_billing.pricing_view`
- **Route**: `path('pricing/', pricing_view, name='pricing')`

**Features:**
- Tab navigation to switch between Trainer and Organization plans
- Dynamic pricing display (Monthly & Annual options)
- Feature comparison cards
- Commission rate badges
- Call-to-action buttons:
  - "Start Now" for free tier
  - "Subscribe" for paid tiers
  - "Current Plan" badge for active subscriptions
- FAQ section with toggle functionality
- Fully responsive (mobile-first design)
- RTL Arabic layout with English fallback

**Page Sections:**
```
┌─ Hero Section ──────────────────┐
│  خطط الاشتراك والأسعار            │
│  Subscription Plans & Pricing   │
└─────────────────────────────────┘
     ↓
┌─ Tab Navigation ────────────────┐
│ [خطط المدربين] [خطط الأندية]    │
│ [Trainer Plans] [Organization]  │
└─────────────────────────────────┘
     ↓
┌─ Pricing Cards Grid ────────────┐
│ ┌─ Plan 1 ──┐ ┌─ Plan 2 ──┐  │
│ │ Price     │ │ Price     │  │
│ │ Features  │ │ Features  │  │
│ │ CTA Button│ │ CTA Button│  │
│ └───────────┘ └───────────┘  │
└─────────────────────────────────┘
     ↓
┌─ FAQ Section ──────────────────┐
│ Question 1 [+] / [-]            │
│ Question 2 [+] / [-]            │
│ Question 3 [+] / [-]            │
└─────────────────────────────────┘
```

**Data Context:**
```python
{
    'trainer_plans': [
        SubscriptionPlan(name='Basic', price=0, is_org_plan=False),
        SubscriptionPlan(name='Premium', price=99, is_org_plan=False),
        # ...
    ],
    'organization_plans': [
        SubscriptionPlan(name='Club', price=500, is_org_plan=True),
        SubscriptionPlan(name='Gold Club', price=1200, is_org_plan=True),
        # ...
    ],
    'user_subscription': TrainerSubscription or Organization (if authenticated),
}
```

**Tab Switching JavaScript:**
```javascript
// Tabs are switched via showTab('trainers' or 'organizations') function
// Uses CSS display property for tab content visibility
// Responsive on mobile (stacked layout)
```

---

### 2. **Clubs Directory Page** (`/clubs/`)
- **File**: `templates/clubs_directory.html`
- **View**: `core.views_billing.clubs_directory_view`
- **Route**: `path('clubs/', clubs_directory_view, name='clubs_directory')`

**Features:**
- Search functionality (club name/keyword search)
- City filter (dropdown with all available cities)
- Active filter tags display
- Pagination (configured as per settings)
- Club cards grid with:
  - Club image/logo with fallback
  - Club name and location
  - Stats badge: trainer count, booking count, average rating
  - "View Club" CTA linking to club detail page
- Fully responsive grid (3 columns desktop, 1 column mobile)
- RTL Arabic layout

**Page Sections:**
```
┌─ Search & Filter Section ──────┐
│ ┌──────────────────────────┐   │
│ │ Search input             │   │
│ │ [Search] [City Filter]   │   │
│ │ [Submit Button]          │   │
│ └──────────────────────────┘   │
└────────────────────────────────┘
     ↓
┌─ Active Filters Display ────────┐
│ [Search: "yoga"] × [City: Cairo] × │
└────────────────────────────────┘
     ↓
┌─ Club Cards Grid ──────────────┐
│ ┌─Club 1──┐ ┌─Club 2──┐ ┌─Club 3──┐ │
│ │ Image   │ │ Image   │ │ Image   │ │
│ │ Name    │ │ Name    │ │ Name    │ │
│ │ ⭐ 4.5  │ │ ⭐ 4.2  │ │ ⭐ 4.8  │ │
│ │ Stats   │ │ Stats   │ │ Stats   │ │
│ │ [View]  │ │ [View]  │ │ [View]  │ │
│ └────────┘ └────────┘ └────────┘ │
└────────────────────────────────┘
     ↓
┌─ Pagination ───────────────────┐
│ [← Previous] [1] [2] [3] [Next →] │
└────────────────────────────────┘
```

**Data Context:**
```python
{
    'clubs': Page(
        [
            Organization(name='Club Name', city='Cairo', logo_image),
            # ... paginated
        ]
    ),
    'search_term': 'search_query' or None,
    'city_filter': 'city_name' or None,
    'all_cities': ['Cairo', 'Fes', 'Marrakech', ...],
    'page_obj': Page object for pagination,
}
```

**Search & Filter Logic:**
```python
# In views_billing.py
queryset = Organization.objects.filter(is_active=True)

if search_term:
    queryset = queryset.filter(
        Q(name__icontains=search_term) |
        Q(description__icontains=search_term) |
        Q(location__icontains=search_term)
    )

if city_filter:
    queryset = queryset.filter(city__iexact=city_filter)

# Apply pagination and sorting
clubs = paginator.get_page(page_number)
```

---

### 3. **Club Detail Page** (`/club/<uuid:club_id>/`)
- **File**: `templates/club_detail.html`
- **View**: `core.views_billing.club_detail_view`
- **Route**: `path('club/<uuid:club_id>/', club_detail_view, name='club_detail')`

**Features:**
- Hero section with club image/logo
- Club info overlay (name, location, subscription tier badge)
- Key stats bar:
  - Total trainers count
  - Total bookings count
  - Club founded year
  - Average rating
- About section with club description
- Contact information:
  - Phone number with WhatsApp link
  - Email address
  - Physical address
- Embedded Google Maps showing club location
- Trainer grid displaying:
  - Trainer profile image
  - Name and specialties (badges)
  - Average rating (star display + review count)
  - Price per hour
  - "Book Now" CTA linking to trainer detail page
- Related clubs sidebar (3 suggested clubs from same city)
- Fully responsive design
- RTL Arabic layout

**Page Sections:**
```
┌─ Hero Section ─────────────────────┐
│ ┌──────────────────────────────┐   │
│ │         Club Image            │   │
│ │    ┌──────────────────┐      │   │
│ │    │ Club Name        │      │   │
│ │    │ Location  | ⭐4.5 │      │   │
│ │    │ Premium Plan     │      │   │
│ │    └──────────────────┘      │   │
│ └──────────────────────────────┘   │
└────────────────────────────────────┘
     ↓
┌─ Stats Bar ────────────────────────┐
│ 👥 15 Trainers | 📅 234 Bookings │
│ ⭐ 4.5 Rating | 📅 Since 2020     │
└────────────────────────────────────┘
     ↓
┌─ About Section ────────────────────┐
│ About the Club                      │
│ Club description text...            │
└────────────────────────────────────┘
     ↓
┌─ Contact & Map Section ────────────┐
│ ┌────────────────────────────────┐ │
│ │ Contact Info      │   Map       │ │
│ │ 📞 +212...       │   [Embed]   │ │
│ │ 📧 club@...      │             │ │
│ │ 📍 Address       │             │ │
│ │ [WhatsApp]       │             │ │
│ └────────────────────────────────┘ │
└────────────────────────────────────┘
     ↓
┌─ Trainers Section ─────────────────┐
│ Available Trainers                  │
│ ┌─Trainer1─┐ ┌─Trainer2─┐ ┌─Trainer3─┐ │
│ │ Avatar    │ │ Avatar    │ │ Avatar    │ │
│ │ Name      │ │ Name      │ │ Name      │ │
│ │ 🏋️ Fitness│ │ 🧘 Yoga   │ │ 💪 CrossFit│ │
│ │ ⭐⭐⭐ (5)│ │ ⭐⭐⭐⭐(8)│ │ ⭐⭐⭐⭐(6)│ │
│ │ 100 MAD/h │ │ 150 MAD/h │ │ 120 MAD/h │ │
│ │ [Book]    │ │ [Book]    │ │ [Book]    │ │
│ └───────────┘ └───────────┘ └───────────┘ │
└────────────────────────────────────┘
     ↓
┌─ Related Clubs Sidebar ────────────┐
│ More Clubs in Cairo                │
│ ┌─Club 1──────────────────┐       │
│ │ Image | Club Name       │       │
│ │       | ⭐ 4.2 (45)      │       │
│ └─────────────────────────┘       │
│ ┌─Club 2──────────────────┐       │
│ │ Image | Club Name       │       │
│ │       | ⭐ 4.5 (32)      │       │
│ └─────────────────────────┘       │
└────────────────────────────────────┘
```

**Data Context:**
```python
{
    'club': Organization(
        id=uuid,
        name='Club Name',
        city='Cairo',
        location='Address',
        phone='+212...',
        email='club@...',
        description='...',
        logo_image=ImageFieldFile,
        latitude=30.0444,
        longitude=-9.5898,
    ),
    'trainers': Trainer.objects.filter(organization=club),
    'related_clubs': Organization.objects.filter(
        city=club.city, 
        is_active=True
    ).exclude(id=club.id)[:3],
}
```

**Trainer Rating Calculation:**
```python
# In club_detail_view
for trainer in trainers:
    reviews = Review.objects.filter(trainer=trainer)
    trainer.avg_rating = avg(review.rating for review in reviews)
    trainer.review_count = len(reviews)
    trainer.specialties = [skill.name for skill in trainer.profile.skills.all()]
```

---

## Database Schema Integration

### Models Used

1. **SubscriptionPlan** (`payments/models.py`)
   ```python
   - name: str (Basic, Premium, Club, Gold Club)
   - price: Decimal (0, 99, 500, 1200 MAD)
   - is_org_plan: bool (True for Club/Gold Club, False for Basic/Premium)
   - max_trainers: int (10, 50)
   - commission_rate: Decimal (20%, 15%, 12%)
   - features: JSONField (list of feature strings)
   ```

2. **Organization** (`payments/models.py`)
   ```python
   - id: UUID (primary key)
   - owner: FK(User)
   - subscription_plan: FK(SubscriptionPlan)
   - name: str
   - city: str
   - location: str (address)
   - phone: str
   - email: str
   - logo_image: ImageField
   - description: TextField
   - latitude: Decimal (for map)
   - longitude: Decimal (for map)
   - is_active: bool
   - created_at: DateTime
   ```

3. **Trainer** (`trainers/models.py`)
   ```python
   - user: OneToOne(CustomUser)
   - organization: FK(Organization) [NEW - for club affiliation]
   - profile: OneToOne(TrainerProfile)
   - specialties: M2M(Specialty)
   - avg_rating: property (calculated from Review)
   ```

4. **TrainerProfile** (`trainers/models.py`)
   ```python
   - price_per_hour: Decimal
   - bio: TextField
   - skills: M2M(Skill)
   ```

5. **Review** (`reviews/models.py`)
   ```python
   - trainer: FK(Trainer)
   - rating: int (1-5)
   - comment: TextField
   - created_at: DateTime
   ```

---

## URL Routing

All routes registered in `fitness_morocco/urls.py`:

```python
urlpatterns = [
    # ... existing routes ...
    
    # New Billing Frontend Routes
    path('pricing/', pricing_view, name='pricing'),
    path('clubs/', clubs_directory_view, name='clubs_directory'),
    path('club/<uuid:club_id>/', club_detail_view, name='club_detail'),
    
    # API Routes
    path('api/billing/', include('payments.urls')),
]
```

---

## Navigation Integration

The navbar (`templates/navbar.html`) has been updated with navigation links:

**Desktop Menu:**
```html
<a href="{% url 'clubs_directory' %}">الأندية (Clubs)</a>
<a href="{% url 'pricing' %}">الأسعار (Pricing)</a>
```

**Mobile Menu:**
```html
<a href="{% url 'clubs_directory' %}">
    <i class="fas fa-building"></i> الأندية
</a>
<a href="{% url 'pricing' %}">
    <i class="fas fa-tag"></i> الأسعار
</a>
```

---

## Frontend Features & Functionality

### 1. Responsive Design
- **Desktop**: 3-column grid for club cards, full-width hero sections
- **Tablet**: 2-column grid, adjusted spacing
- **Mobile**: Single column, stacked layout, optimized touch targets

### 2. Arabic/RTL Support
- All text wrapped with Arabic translations
- Flexbox with `space-x-reverse` for RTL layout
- Icon positioning adjusted for RTL (ml-2 for left margin in RTL context)
- Date and time formatting respects locale
- Currency symbol placement (MAD after amount)

### 3. Interactive Elements
- Tab switching with JavaScript (no page reload)
- FAQ toggle with smooth height animation
- Mobile menu hamburger toggle
- Search form with live filtering
- City dropdown with all available options
- Pagination with next/previous buttons

### 4. Performance Optimization
- Lazy loading for images (when supported)
- CSS optimized for Tailwind production build
- Minimal JavaScript (vanilla JS, no jQuery)
- Database queries optimized with select_related/prefetch_related

### 5. Accessibility
- Semantic HTML structure
- ARIA labels on buttons and links
- Keyboard navigation support
- Color contrast meets WCAG standards
- Font sizes responsive and readable

---

## Testing the Integration

### 1. Test Pricing Page
```bash
curl http://localhost:8000/pricing/
```

Expected response: HTML page with pricing cards, tabs, FAQ

### 2. Test Clubs Directory
```bash
curl http://localhost:8000/clubs/
curl http://localhost:8000/clubs/?search=yoga&city=Cairo
```

Expected response: HTML page with club cards, search form, pagination

### 3. Test Club Detail
```bash
curl http://localhost:8000/club/<organization_uuid>/
```

Expected response: HTML page with club info, trainers, map, related clubs

### 4. Test Navigation
- Visit homepage and check navbar has pricing/clubs links
- Click links and verify navigation works
- Test responsive menu on mobile viewport

---

## Common Issues & Solutions

### Issue: Club not showing trainers
**Solution**: Ensure trainer has `organization` field set in admin panel
```python
Trainer.objects.filter(organization=club)
```

### Issue: Map not embedding
**Solution**: Verify club has `latitude` and `longitude` set
```python
club.latitude, club.longitude  # Must be valid coordinates
```

### Issue: Pagination not working
**Solution**: Ensure page number is passed and validated
```python
page = request.GET.get('page', 1)
paginator = Paginator(clubs, 12)  # 12 clubs per page
page_obj = paginator.get_page(page)
```

### Issue: Search not filtering
**Solution**: Check that search term is URL-encoded properly
```python
search_term = request.GET.get('search', '').strip()
if search_term:
    queryset = queryset.filter(Q(...) | Q(...))
```

### Issue: Arabic text not displaying correctly
**Solution**: Ensure `<meta charset="UTF-8">` in base template and `dir="rtl"` on body
```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    ...
</head>
```

---

## Next Steps - Frontend Enhancements

### Phase 2 - Organization Management
1. Create organization creation form page
2. Organization settings/profile edit page
3. Add trainer to organization form
4. Trainer invitation management UI

### Phase 3 - Subscription Management
1. Trainer subscription status dashboard
2. Plan upgrade/downgrade flow
3. Billing history & invoice viewing
4. Earnings dashboard for trainers

### Phase 4 - Payment Integration
1. Stripe checkout integration
2. Payment success/failure handling
3. Subscription renewal flow
4. Email confirmations

### Phase 5 - Advanced Features
1. Analytics dashboard for gym owners
2. Commission tracking UI
3. Seat management interface
4. Trainer performance insights

---

## File Summary

| File | Lines | Purpose |
|------|-------|---------|
| `templates/pricing.html` | 400+ | Pricing page with tabs and FAQ |
| `templates/clubs_directory.html` | 350+ | Club directory with search/filter |
| `templates/club_detail.html` | 400+ | Club landing page with trainers |
| `core/views_billing.py` | 300+ | View functions for billing pages |
| `templates/navbar.html` | Updated | Navigation links added |
| `fitness_morocco/urls.py` | Updated | Routes for new pages |

---

## Deployment Checklist

- [ ] All database migrations applied
- [ ] Static files collected
- [ ] Images uploaded to server
- [ ] Environment variables set (if needed)
- [ ] Email notifications configured
- [ ] Stripe webhooks configured
- [ ] DNS records updated
- [ ] SSL certificate configured
- [ ] Backup strategy in place
- [ ] Monitoring and logging enabled

---

End of Frontend Integration Guide
