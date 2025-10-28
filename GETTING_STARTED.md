# 🎯 NEXT STEPS - Get Started with EduTrack AI

## ⚡ Quick Start (3 Steps)

### Step 1: Add API Keys
Edit the `.env` file in the project root:
```bash
nano .env
```

Add your API credentials:
```env
GITHUB_TOKEN=ghp_your_github_token_here
GEMINI_API_KEY=AIza_your_gemini_key_here
```

**Where to get API keys:**
- 🔑 GitHub Token: https://github.com/settings/tokens
  - Click "Generate new token (classic)"
  - Select scope: `repo` (Full control of private repositories)
  - Copy the token
  
- 🔑 Gemini API Key: https://makersuite.google.com/app/apikey
  - Click "Create API key"
  - Copy the key

### Step 2: Create Admin Account
```bash
uv run python manage.py createsuperuser
```

Enter:
- Username: (your choice)
- Email: (optional)
- Password: (your choice)

### Step 3: Start Server
```bash
./run.sh
```

Or manually:
```bash
uv run python manage.py runserver
```

🌐 **Visit:** http://127.0.0.1:8000

---

## 📋 First Time Usage Guide

### 1. Register/Login
- Go to http://127.0.0.1:8000
- Click "Register" to create account
- Or use superuser credentials

### 2. Create Your First Assignment
- Click "Create Assignment"
- Fill in:
  - Title: "Week 1 - Python Basics"
  - Description: "Build a calculator"
  - Deadline: (optional)
- Click "Create"

### 3. Add Student Repositories

**Option A: Single Add**
- Click "Add Repository"
- Enter:
  - Student Name: "John Doe"
  - GitHub URL: "https://github.com/johndoe/calculator"
- Click "Add Repository"

**Option B: Bulk Add**
- Click "Bulk Add Repositories"
- Enter multiple lines:
  ```
  John Doe, https://github.com/johndoe/calculator
  Jane Smith, https://github.com/janesmith/calc-project
  Bob Wilson, https://github.com/bobwilson/python-calc
  ```
- Click "Add Repositories"

### 4. Analyze Repositories
- Click "Analyze" button next to any repository
- Wait for processing (5-10 seconds)
- View results!

### 5. View Detailed Analysis
- Click "View" to see:
  - AI-generated summary
  - Strengths and improvements
  - Performance score (0-100)
  - Language breakdown
  - Commit history
  - README preview

---

## 🧪 Test with Sample Data

Want to test without real student data? Use these public repositories:

```
Test Student 1, https://github.com/microsoft/vscode
Test Student 2, https://github.com/django/django
Test Student 3, https://github.com/python/cpython
```

---

## 📊 Admin Panel

Access the Django admin at: http://127.0.0.1:8000/admin

Login with your superuser credentials to:
- Manage all assignments
- View all student repositories
- Check analysis logs
- Manage users

---

## 🔧 Useful Commands

### Development
```bash
# Start server
./run.sh

# Or with auto-reload
uv run python manage.py runserver

# Access Django shell
uv run python manage.py shell
```

### Database
```bash
# Create new migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Reset database (WARNING: deletes all data)
rm db.sqlite3
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

### Package Management
```bash
# Add new package
uv add requests beautifulsoup4

# Remove package
uv remove package-name

# Sync dependencies
uv sync

# Update all packages
uv sync --upgrade
```

---

## 🎨 Customize the Application

### Change Colors
Edit `edutrack/templates/base.html`, find:
```css
:root {
    --primary-color: #4f46e5;
    --secondary-color: #7c3aed;
}
```

### Modify Templates
All templates are in: `edutrack/templates/`
- `home.html` - Landing page
- `dashboard.html` - Teacher dashboard
- `assignment_detail.html` - Assignment view
- etc.

### Add Custom Static Files
Place files in:
- `edutrack/static/css/` - Custom CSS
- `edutrack/static/js/` - Custom JavaScript

---

## 🚀 Deploy to Production

### Quick Deploy Options

**1. Render (Recommended)**
- Create account at https://render.com
- Connect your GitHub repo
- Set environment variables
- Deploy!

**2. Railway**
- https://railway.app
- One-click deploy from GitHub

**3. PythonAnywhere**
- https://pythonanywhere.com
- Free tier available

### Before Deploying
```bash
# Set DEBUG to False in .env
DEBUG=False

# Add your domain to ALLOWED_HOSTS in settings.py
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Collect static files
uv run python manage.py collectstatic
```

---

## ❓ Troubleshooting

### "No module named 'packaging'"
```bash
uv add packaging
```

### "CSRF verification failed"
- Clear browser cookies
- Check `.env` file exists

### "Connection refused" when analyzing
- Check GitHub token in `.env`
- Check Gemini API key in `.env`
- Verify internet connection

### Static files not loading
```bash
uv run python manage.py collectstatic
```

### Database locked error
```bash
# Stop all running servers
# Then:
rm db.sqlite3
uv run python manage.py migrate
```

---

## 📱 Access from Other Devices

To access from phone/tablet on same network:
```bash
# Find your IP address
hostname -I

# Start server on all interfaces
uv run python manage.py runserver 0.0.0.0:8000

# Access from other devices
http://YOUR_IP_ADDRESS:8000
```

---

## 🎓 Learn More

- **Django Tutorial:** https://docs.djangoproject.com/en/stable/intro/tutorial01/
- **GitHub API Docs:** https://docs.github.com/en/rest
- **Gemini AI Docs:** https://ai.google.dev/tutorials/python_quickstart
- **uv Documentation:** https://docs.astral.sh/uv/

---

## ✅ Checklist

- [ ] Added GitHub token to `.env`
- [ ] Added Gemini API key to `.env`
- [ ] Created superuser account
- [ ] Started the server successfully
- [ ] Registered a regular user account
- [ ] Created first assignment
- [ ] Added test repository
- [ ] Ran first analysis
- [ ] Viewed detailed results

---

## 🎉 You're Ready!

Everything is set up and ready to go. Just:

1. **Add API keys** to `.env`
2. **Create superuser**: `uv run python manage.py createsuperuser`
3. **Start server**: `./run.sh`
4. **Visit**: http://127.0.0.1:8000

**Happy tracking!** 🚀👨‍🏫
