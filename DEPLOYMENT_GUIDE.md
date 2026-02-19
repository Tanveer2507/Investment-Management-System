# Deployment Guide - Investment Management System

## 🚀 Deploy on Render.com (Recommended - Free Tier)

### Step 1: Prepare Repository
1. Push all code to GitHub
2. Make sure all files are committed

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account

### Step 3: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Tanveer2507/Investment-Management-System`
3. Configure:
   - **Name**: investment-management-system
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn investment_system.wsgi:application`
   - **Plan**: Free

### Step 4: Add Environment Variables
In Render dashboard, add these environment variables:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your site will be live at: `https://your-app-name.onrender.com`

---

## 🐍 Deploy on PythonAnywhere (Alternative - Free Tier)

### Step 1: Create Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account

### Step 2: Clone Repository
Open Bash console and run:
```bash
git clone https://github.com/Tanveer2507/Investment-Management-System.git
cd Investment-Management-System
```

### Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Python 3.10

### Step 5: Configure WSGI
Edit WSGI configuration file:
```python
import os
import sys

path = '/home/yourusername/Investment-Management-System'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'investment_system.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Set Static Files
In Web tab:
- URL: `/static/`
- Directory: `/home/yourusername/Investment-Management-System/static/`

### Step 7: Run Migrations
In Bash console:
```bash
cd Investment-Management-System
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### Step 8: Reload
Click "Reload" button in Web tab

Your site will be live at: `https://yourusername.pythonanywhere.com`

---

## 📋 Pre-Deployment Checklist

- [x] requirements.txt created
- [x] Procfile created
- [x] runtime.txt created
- [x] .gitignore created
- [x] Settings updated for production
- [ ] Push to GitHub
- [ ] Create Render/PythonAnywhere account
- [ ] Deploy following steps above

---

## 🔧 Post-Deployment

1. **Create Superuser**:
```bash
python manage.py createsuperuser
```

2. **Test the site**:
   - Visit homepage
   - Test login/register
   - Test all features

3. **Update README.md**:
   - Replace `https://your-website-url.com` with actual URL

4. **Add to GitHub**:
   - Go to repository settings
   - Add website URL in "About" section

---

## 🆘 Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Database errors
```bash
python manage.py migrate
```

### Server errors
Check logs in Render/PythonAnywhere dashboard

---

## 📞 Support

For deployment issues:
- Render Docs: https://render.com/docs
- PythonAnywhere Help: https://help.pythonanywhere.com
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Note**: Free tier has limitations:
- Render: App sleeps after 15 min inactivity
- PythonAnywhere: Limited CPU/bandwidth

For production use, consider paid plans.
