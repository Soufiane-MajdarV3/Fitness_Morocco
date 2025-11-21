# MySQL Database Setup Guide for Josted Hosting

## Step 1: Find Your MySQL Host Information

Please check your Josted hosting control panel (cPanel/Plesk) and find:

1. **MySQL Server Host**: This is usually something like:
   - `mysql.josted.com` or `sql.josted.com`
   - Or a specific IP address provided by Josted
   - Check under: Database Management → MySQL Databases

2. **Database Name**: `u386073008_fitness_morocc` ✓ (Already have this)

3. **MySQL Username**: `u386073008_fitness_admin` ✓ (Already have this)

4. **MySQL Password**: `?M5Jh2NWSi` ✓ (Already have this)

5. **MySQL Port**: Usually `3306` (default), but check if Josted uses a different port

## Step 2: Update Django Settings

Once you have the MySQL host, update the file:
**File**: `/home/sofiane/Desktop/SaaS/Fitness/fitness_morocco/settings.py`

Find the DATABASES section and replace the HOST with your Josted MySQL host:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'u386073008_fitness_morocc',
        'USER': 'u386073008_fitness_admin',
        'PASSWORD': '?M5Jh2NWSi',
        'HOST': 'YOUR_MYSQL_HOST_HERE',  # Get this from Josted cPanel
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

## Step 3: Test Database Connection

Once you've updated the HOST, run:

```bash
cd /home/sofiane/Desktop/SaaS/Fitness
python3 manage.py check
```

If successful, you'll see: `System check identified no issues (0 silenced)`

## Step 4: Run Migrations

```bash
python3 manage.py migrate
```

This will create all database tables.

## Step 5: Populate Database

Run the data population script:

```bash
python3 manage.py populate_db
```

This will create:
- 6 cities
- 8 session types
- 10 trainers (with full profiles)
- 15 clients
- 40+ bookings with reviews
- 5 gyms

## Step 6: Create Admin User

```bash
python3 manage.py createsuperuser
```

Then access admin at: `http://yourdomain.com/admin/`

## Step 7: Start the Server

```bash
python3 manage.py runserver
```

Access at: `http://localhost:8000/`

---

## Common Issues & Solutions

### Issue: "Can't connect to MySQL server"
**Solution**: Make sure you have the correct MySQL HOST from Josted

### Issue: "Access denied for user"
**Solution**: Verify username and password are correct from Josted panel

### Issue: "Port 3306 refused"
**Solution**: Check if Josted uses a different port (might be 3307, 3308, etc.)

### Issue: "Database already exists"
**Solution**: That's fine, migrations will work on existing database

---

## After Setup - Default Login Credentials

Once you run `populate_db`, you can login with:

**Trainer Account:**
- Username: `trainer_محمد_علي` 
- Password: `trainer123`

**Client Account:**
- Username: `client_أحمد_محمود`
- Password: `client123`

**Admin:**
- Username/Password: (created with createsuperuser command)

---

## Quick Commands Reference

```bash
# Check setup
python3 manage.py check

# Run migrations
python3 manage.py migrate

# Populate database
python3 manage.py populate_db

# Create admin user
python3 manage.py createsuperuser

# Start server
python3 manage.py runserver

# Access admin panel
# http://localhost:8000/admin/
```

---

**Need Help?** Check your Josted cPanel for MySQL connection details, then update the HOST in settings.py
