# Fitness Morocco - Vercel Deployment Guide

## Prerequisites
- Vercel account (vercel.com)
- GitHub account with your repository
- MySQL database (already configured on Josted)
- Domain name (optional but recommended)

## Step 1: Prepare Your Repository

```bash
# Initialize Git if not already done
git init
git add .
git commit -m "Initial commit - ready for Vercel deployment"

# Push to GitHub
git remote add origin https://github.com/your-username/fitness-morocco.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard (Recommended)

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Configure project settings:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Output Directory: `staticfiles`
   - Install Command: `pip install -r requirements.txt`

5. Add Environment Variables in Vercel Dashboard:
   - `ENVIRONMENT` = `production`
   - `SECRET_KEY` = Generate a new secure key: https://djecrety.ir/
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `your-domain.vercel.app,www.your-domain.vercel.app`
   - `CSRF_TRUSTED_ORIGINS` = `https://your-domain.vercel.app,https://www.your-domain.vercel.app`
   - `DB_NAME` = `u386073008_fitness_morocc`
   - `DB_USER` = `u386073008_fitness_admin`
   - `DB_PASSWORD` = `?M5Jh2NWSi`
   - `DB_HOST` = `auth-db1815.hstgr.io`
   - `DB_PORT` = `3306`

6. Click "Deploy"

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Follow the prompts and add environment variables as above
```

## Step 3: Connect Your Domain (Optional)

1. In Vercel Dashboard, go to your project
2. Go to Settings → Domains
3. Add your custom domain
4. Update your domain's DNS settings according to Vercel's instructions

## Step 4: Post-Deployment Configuration

After deployment, run migrations:

```bash
# Via Vercel Deployment Hooks or manually
vercel env pull .env.local
DJANGO_SETTINGS_MODULE=fitness_morocco.settings_vercel python manage.py migrate
```

## Environment Variables Setup

Create a `.env` file in your project root (don't commit this):

```
DEBUG=False
SECRET_KEY=your-very-secure-key-here
ENVIRONMENT=production
ALLOWED_HOSTS=your-domain.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-domain.vercel.app
DB_NAME=u386073008_fitness_morocc
DB_USER=u386073008_fitness_admin
DB_PASSWORD=?M5Jh2NWSi
DB_HOST=auth-db1815.hstgr.io
DB_PORT=3306
```

## Project Structure for Vercel

```
fitness-morocco/
├── api/
│   └── index.py              # WSGI entry point
├── fitness_morocco/
│   ├── settings.py           # Development settings
│   ├── settings_vercel.py    # Production settings
│   ├── wsgi.py
│   └── ...
├── templates/                # Django templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User uploads
├── manage.py
├── requirements.txt
├── vercel.json              # Vercel configuration
├── .env.example             # Environment variables example
├── build.sh                 # Build script
└── ...
```

## Important Notes

1. **Database Connection**: Your MySQL database is hosted on Josted. Make sure it's accessible from Vercel's servers.

2. **Static Files**: Use WhiteNoise middleware to serve static files efficiently.

3. **Media Files**: For user uploads, consider using cloud storage (AWS S3, Cloudinary, etc.) instead of local filesystem.

4. **Database Migrations**: Migrations run automatically during build. If issues occur:
   ```bash
   vercel env pull .env.local
   DJANGO_SETTINGS_MODULE=fitness_morocco.settings_vercel python manage.py migrate --run-syncdb
   ```

5. **Admin Panel**: Your admin panel will be available at:
   ```
   https://your-domain.vercel.app/admin/
   ```

6. **Superuser**: Create a superuser for admin access:
   ```bash
   DJANGO_SETTINGS_MODULE=fitness_morocco.settings_vercel python manage.py createsuperuser
   ```

## Troubleshooting

### Static Files Not Loading
- Ensure `STATIC_ROOT` is set to `staticfiles/`
- Run: `python manage.py collectstatic --noinput`
- Check that files are in the `staticfiles/` directory

### Database Connection Failed
- Verify MySQL host is accessible from Vercel
- Check database credentials in environment variables
- Ensure your Josted firewall allows connections

### Import Errors
- Install missing packages in `requirements.txt`
- Ensure all apps are listed in `INSTALLED_APPS`
- Check Python version compatibility (3.11+)

### CSS/Images Not Appearing
- Check static files path in browser DevTools
- Run `python manage.py collectstatic --clear --noinput`
- Clear Vercel cache: go to Settings → Git → Clear Build Cache

## Monitoring & Maintenance

1. **View Logs**:
   ```bash
   vercel logs
   ```

2. **Check Deployments**:
   - Vercel Dashboard → Deployments tab

3. **Performance**:
   - Monitor database query times
   - Use Django Debug Toolbar locally to identify bottlenecks

4. **Backups**:
   - Regularly backup your MySQL database
   - Keep database credentials secure

## Rollback to Previous Version

```bash
vercel rollback
```

## Next Steps

1. Test all features in production
2. Set up monitoring and error tracking (Sentry)
3. Configure email notifications
4. Set up analytics
5. Document any custom domain setup

## Support

- Vercel Documentation: https://vercel.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Josted MySQL: https://www.hstgr.io/
