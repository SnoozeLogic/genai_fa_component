# 📚 Quick Reference Guide - GENAI FA Component

## 🚀 Quick Commands

### Start Application
```bash
./start.sh                              # Recommended
uv run python manage.py runserver       # Manual
uv run python manage.py runserver 8080  # Custom port
```

### Database
```bash
uv run python manage.py migrate              # Apply migrations
uv run python manage.py makemigrations       # Create migrations
uv run python manage.py createsuperuser      # Create admin user
uv run python manage.py shell                # Django shell
```

### Package Management
```bash
uv sync                  # Install dependencies
uv add package-name      # Add new package
uv remove package-name   # Remove package
uv sync --refresh        # Refresh lock file
```

### Troubleshooting
```bash
pkill -f runserver                     # Kill server
rm db.sqlite3 && python manage.py migrate  # Reset database
rm -rf .venv uv.lock && uv sync       # Clean install
```

---

## 📖 Common URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Dashboard | http://127.0.0.1:8000/dashboard/ |
| Login | http://127.0.0.1:8000/login/ |
| Register | http://127.0.0.1:8000/register/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |
| Create Assignment | http://127.0.0.1:8000/assignments/create/ |
| Assignment List | http://127.0.0.1:8000/assignments/ |

---

## 🎯 Workflow Quick Guide

### 1️⃣ Create Assignment
1. Dashboard → "Create New Assignment"
2. Fill: Title, Description, Deadline
3. Click "Create"

### 2️⃣ Add Repositories
**Single:**
1. Open assignment → "Add Repository"
2. Enter: Student name, GitHub URL
3. Click "Add"

**Bulk:**
1. Open assignment → "Bulk Upload"
2. Upload CSV: `Name, URL`
3. Confirm

### 3️⃣ Analyze Repository
1. Click "Analyze" button
2. Wait 10-30 seconds
3. View results

### 4️⃣ View Results
- Click student name to see full analysis
- Check dashboard for statistics
- Review analytics page for trends

---

## 🔧 Environment Variables

```env
# Required
GEMINI_API_KEY=your_key_here
SECRET_KEY=django_secret_key

# Optional
GITHUB_TOKEN=your_token_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 📊 Feature Checklist

### Core Features
- ✅ Assignment management
- ✅ Repository tracking
- ✅ AI-powered analysis (Gemini 2.5 Pro)
- ✅ GitHub data extraction
- ✅ Performance scoring (0-100)
- ✅ Dashboard with statistics
- ✅ Analytics overview
- ✅ Bulk repository upload (CSV)
- ✅ Markdown-formatted AI responses
- ✅ Contributor tracking

### UI Features
- ✅ Responsive design
- ✅ Bootstrap 5
- ✅ Gradient color scheme
- ✅ Progress indicators
- ✅ Status badges
- ✅ Interactive cards
- ✅ Modern footer with badges

---

## 🐛 Quick Fixes

### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

### Reset Database
```bash
rm db.sqlite3
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

### Gemini API Issues
1. Check `.env` file has correct key
2. Verify quota at https://makersuite.google.com
3. Check terminal for `[SCORE DEBUG]` messages

### Score Not Extracting
- View terminal output during analysis
- Look for `[SCORE DEBUG]` messages
- Ensure Gemini response includes score (X/100 or Score: X)

### Dependencies Not Syncing
```bash
rm -rf .venv uv.lock
uv sync
```

---

## 📈 Performance Stats

| Operation | Time |
|-----------|------|
| Analysis per repo | 10-30 sec |
| GitHub API call | <1 sec |
| Dashboard load | <500ms |
| Bulk upload (10 repos) | ~1 sec |

---

## 🎨 Color Scheme

| Element | Color |
|---------|-------|
| Primary | #667eea (Purple) |
| Secondary | #764ba2 (Indigo) |
| Success | #28a745 (Green) |
| Warning | #ffc107 (Orange) |
| Danger | #dc3545 (Red) |
| Info | #17a2b8 (Cyan) |

---

## 📝 CSV Format for Bulk Upload

```csv
Student Name, Repository URL
John Doe, https://github.com/johndoe/project
Jane Smith, https://github.com/janesmith/app
Bob Wilson, https://github.com/bobw/assignment1
```

**Requirements:**
- Header row required
- Two columns: Name, URL
- HTTPS GitHub URLs
- One repository per line

---

## 🔑 API Keys Guide

### Gemini API
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Create API key
4. Add to `.env`: `GEMINI_API_KEY=...`

### GitHub Token (Optional)
1. Visit: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scope: `repo`
4. Add to `.env`: `GITHUB_TOKEN=...`

**Note:** GitHub token only needed for private repositories.

---

## 📦 Project Files

```
Important Files:
├── .env                 # Environment configuration
├── manage.py            # Django management
├── start.sh            # Startup script
├── README.md           # Full documentation
├── config/settings.py  # Django settings
├── edutrack/views.py   # Main logic
└── edutrack/models.py  # Database models
```

---

## 🎓 Models Overview

### Assignment
- teacher (User)
- title (CharField)
- description (TextField)
- deadline (DateTimeField)
- created_at, updated_at

### StudentRepo
- assignment (ForeignKey)
- student_name (CharField)
- repo_url (URLField)
- commit_count (Integer)
- languages (JSON)
- contributors (JSON)
- ai_summary (Text)
- performance_score (Float)
- is_analyzed (Boolean)

### AnalysisLog
- repo (ForeignKey)
- status (success/failed)
- error_message (Text)
- analyzed_at (DateTime)

---

## 🔒 Security Checklist

Development:
- ✅ DEBUG = True
- ✅ SQLite database
- ✅ Test credentials

Production:
- [ ] DEBUG = False
- [ ] Change SECRET_KEY
- [ ] PostgreSQL/MySQL
- [ ] HTTPS enabled
- [ ] ALLOWED_HOSTS configured
- [ ] Static files served
- [ ] Backups configured
- [ ] Monitoring set up

---

## 📞 Quick Links

- **Documentation**: `/docs` folder
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **GitHub Repo**: https://github.com/SnoozeLogic/genai_fa_component
- **Issues**: https://github.com/SnoozeLogic/genai_fa_component/issues

---

## 💡 Tips & Tricks

1. **Use Bulk Upload**: Faster for multiple students
2. **Set Deadlines**: Get color-coded warnings
3. **Check Analytics**: See overall performance
4. **Use GitHub Token**: Avoid rate limits
5. **Monitor Terminal**: Debug output helps troubleshoot
6. **Regular Backups**: Export database periodically

---

**Last Updated:** October 28, 2025
**Version:** 1.0.0
**Status:** Production Ready
