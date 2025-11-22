# Quick Reference - Subscription & Club Pages

## Pages Summary

### 1. Pricing Page 💰
- **URL**: `/pricing/`
- **File**: `templates/pricing.html`
- **Purpose**: Display subscription plans with pricing and features
- **Features**: Tabs (Trainer/Org), FAQ, CTAs, current plan indicator

### 2. Clubs Directory 🏢
- **URL**: `/clubs/`
- **File**: `templates/clubs_directory.html`
- **Purpose**: Browse all fitness clubs with search and filter
- **Features**: Search, city filter, pagination, club cards, stats

### 3. Club Detail 🏋️
- **URL**: `/club/<uuid:club_id>/`
- **File**: `templates/club_detail.html`
- **Purpose**: View club landing page with trainers
- **Features**: Hero, info, map, trainers, ratings, booking links

---

## URL Routes

```
GET /pricing/                       → Show pricing page
GET /clubs/                         → Show clubs directory
GET /clubs/?search=yoga&city=Cairo  → Search and filter clubs
GET /club/550e8400-e29b-41d4-a716-446655440000/  → Show club detail
```

---

## Navigation Links

**Desktop Navbar**:
- "الأندية" (Clubs) → `/clubs/`
- "الأسعار" (Pricing) → `/pricing/`

**Mobile Navbar**:
- Clubs icon → `/clubs/`
- Pricing icon → `/pricing/`

---

## Data Requirements

### For Pricing Page
- `SubscriptionPlan` objects (auto-populated via init command)
- User's current subscription (if logged in)

### For Clubs Directory
- `Organization` objects with `is_active=True`
- Each club needs: name, city, image (optional)

### For Club Detail
- `Organization` object with:
  - name, city, location, phone, email
  - latitude, longitude (for maps)
  - logo_image, description
- Associated `Trainer` objects
- Trainer profiles with pricing and skills
- `Review` objects for ratings

---

## File Structure

```
templates/
├── pricing.html              (Pricing page)
├── clubs_directory.html      (Club directory)
├── club_detail.html          (Club detail)
├── navbar.html               (Updated with links)
└── base.html                 (Base template)

core/
├── views_billing.py          (View functions)
├── views.py                  (Existing views)
└── urls.py                   (Routing - already updated)

fitness_morocco/
└── urls.py                   (Main URLs - already updated)
```

---

## View Functions

### pricing_view(request)
```python
# Returns:
{
    'trainer_plans': SubscriptionPlan.objects.filter(is_org_plan=False),
    'organization_plans': SubscriptionPlan.objects.filter(is_org_plan=True),
    'user_subscription': user's subscription or None,
}
```

### clubs_directory_view(request)
```python
# Query Parameters:
# - search: string (club name/keywords)
# - city: string (filter by city)
# - page: int (page number)

# Returns:
{
    'clubs': Page object with Organization queryset,
    'search_term': string or None,
    'city_filter': string or None,
    'all_cities': list of city names,
    'page_obj': Django Page object,
}
```

### club_detail_view(request, club_id)
```python
# URL Parameter:
# - club_id: UUID of Organization

# Returns:
{
    'club': Organization object,
    'trainers': Trainer.objects.filter(organization=club),
    'related_clubs': similar clubs from same city,
}
```

---

## Styling & Design

- **Framework**: Tailwind CSS 3.x
- **Icons**: Font Awesome 6.x
- **Language**: Arabic (RTL) + English
- **Responsive**: Mobile-first design
- **Colors**: Indigo/Purple gradient theme

---

## Key Features Implemented

### Pricing Page
✅ Tab navigation
✅ Dynamic pricing cards
✅ Feature comparison
✅ FAQ with toggle
✅ CTA buttons
✅ Current plan badge
✅ Annual discounts
✅ Commission rates

### Clubs Directory
✅ Search functionality
✅ City filter dropdown
✅ Pagination (12 per page)
✅ Club card grid
✅ Stats display
✅ Image fallback
✅ Empty state
✅ Active filters

### Club Detail
✅ Hero section
✅ Info overlay
✅ Stats bar
✅ About section
✅ Contact info
✅ Maps embed
✅ Trainer grid
✅ Ratings/Reviews
✅ Related clubs
✅ Breadcrumbs

---

## Testing URLs

```bash
# Test Pricing Page
curl http://localhost:8000/pricing/

# Test Clubs Directory
curl http://localhost:8000/clubs/
curl "http://localhost:8000/clubs/?search=yoga&city=Cairo"

# Test Club Detail (with valid UUID)
curl http://localhost:8000/club/550e8400-e29b-41d4-a716-446655440000/

# Test Navigation Links
# Visit http://localhost:8000/ and click navbar links
```

---

## API Integration

All pages use existing models via QuerySets:
- `SubscriptionPlan` → pricing data
- `Organization` → club data
- `Trainer` → trainer data
- `TrainerProfile` → pricing & skills
- `Review` → ratings
- `Booking` → booking links

No new APIs created (uses Django ORM directly in views).

---

## Frontend Technologies

- **Templates**: Django Jinja2
- **Styling**: Tailwind CSS
- **JavaScript**: Vanilla JS (minimal)
- **Icons**: Font Awesome
- **Maps**: Google Maps Embed
- **Images**: Django ImageField
- **Internationalization**: Django i18n (Arabic/English)

---

## Performance Optimizations

✅ Lazy loading for images
✅ CSS minified via Tailwind
✅ Minimal JavaScript
✅ Database query optimization
✅ Pagination (limit data transfer)
✅ Cached static files

---

## Responsive Breakpoints

| Device | Width | Layout |
|--------|-------|--------|
| Mobile | < 768px | 1 column |
| Tablet | 768-1024px | 2 columns |
| Desktop | > 1024px | 3 columns |

---

## Arabic/RTL Features

✅ Full Arabic translations
✅ `dir="rtl"` layout
✅ Flexbox with `space-x-reverse`
✅ Icon positioning for RTL
✅ Currency in MAD
✅ Proper font sizing

---

## Common Tasks

### Add New Club
1. Go to Django admin
2. Create new Organization
3. Set name, city, location, phone, email
4. Upload logo image
5. Add trainers to club
6. Club appears in directory

### Update Pricing
1. Go to Django admin
2. Edit SubscriptionPlan
3. Update price, features, commission
4. Changes appear on pricing page automatically

### Add Trainer to Club
1. Go to Django admin
2. Edit Trainer
3. Set organization field to club
4. Trainer appears in club detail page

---

## Troubleshooting

**Club not showing**
→ Check `is_active=True` in admin

**Trainer not in club**
→ Set trainer's `organization` field in admin

**Map not loading**
→ Verify club has `latitude` and `longitude`

**Arabic not RTL**
→ Check `<html lang="ar" dir="rtl">` in template

**Images not loading**
→ Run `python manage.py collectstatic`

---

## Deployment

### Quick Deploy
```bash
# 1. Verify no errors
python manage.py check

# 2. Apply migrations
python manage.py migrate

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Test pages
python manage.py runserver

# 5. Deploy to production
```

---

## Documentation Files

1. **FRONTEND_INTEGRATION_GUIDE.md** - Comprehensive technical guide
2. **FRONTEND_SUMMARY.md** - Implementation summary
3. **VERIFICATION_COMPLETE.md** - Quality assurance report
4. **This file** - Quick reference

---

## Next Steps

1. Add organization creation form
2. Create subscription management dashboard
3. Implement earnings tracking page
4. Add Stripe payment integration
5. Set up email notifications

---

## Quick Links

- Pricing Page: `/pricing/`
- Clubs Directory: `/clubs/`
- Admin Panel: `/admin/`
- Home: `/`
- Trainers: `/trainers/`

---

## Support

For issues or questions:
1. Check documentation files
2. Review view functions in `core/views_billing.py`
3. Check template files for HTML/CSS
4. Verify database models are populated

---

**Status**: ✅ Ready for Production
**Last Updated**: November 22, 2025
**Version**: 1.0
