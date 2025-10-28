# 🚀 EduTrack AI — GenAI-Powered Student Submission Tracker

A comprehensive AI-powered student submission tracking system for educators that integrates **GitHub API** and **Gemini API** to automate repository analysis and provide intelligent feedback.

## 🧠 Overview

**EduTrack AI** helps teachers track student GitHub repositories, analyze code quality, and generate AI-powered insights. The system automatically fetches repository data including commits, languages, README content, and uses Google's Gemini AI to provide performance analysis and constructive feedback.

## 🏗️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Backend:** Django 4.2 with ASGI support
- **Database:** SQLite (default) / PostgreSQL
- **APIs:** 
  - GitHub REST API (for repository data)
  - Google Gemini API (for AI analysis)
- **Server:** Uvicorn (ASGI) / Django Dev Server

## ⚙️ Features

### 👨‍🏫 Teacher Features
- ✅ User authentication (register/login)
- ✅ Create and manage assignments
- ✅ Add student GitHub repositories (single or bulk)
- ✅ Automated repository analysis using AI
- ✅ View detailed analytics and insights
- ✅ Performance scoring (0-100)
- ✅ Track analysis history

### 🔍 GitHub Integration
- Fetch total commits and commit history
- Extract programming languages used
- Get README content
- Identify contributors
- Track latest commit details

### 🧠 AI Analysis (Gemini)
- Code quality summary
- Strength identification
- Areas for improvement
- Performance scoring
- Actionable recommendations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Git
- GitHub Personal Access Token
- Google Gemini API Key

### Quick Setup

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd genai_fa_component
```

2. **Run the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

The script will:
- Create a virtual environment
- Install all dependencies
- Set up the database
- Prompt you to create a superuser

3. **Configure environment variables:**

Edit `.env` file and add your API keys:
```env
GITHUB_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Getting API Keys:**
- **GitHub Token:** https://github.com/settings/tokens (needs `repo` scope)
- **Gemini API Key:** https://makersuite.google.com/app/apikey

4. **Start the development server:**

Option 1 - Django Dev Server:
```bash
source venv/bin/activate
python manage.py runserver
```

Option 2 - Uvicorn (ASGI):
```bash
source venv/bin/activate
uvicorn config.asgi:application --reload
```

5. **Access the application:**

Open your browser and visit: http://127.0.0.1:8000

## 📁 Project Structure

```
genai_fa_component/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings
│   ├── urls.py            # URL routing
│   ├── asgi.py            # ASGI config
│   └── wsgi.py            # WSGI config
├── edutrack/              # Main Django app
│   ├── api/               # API handlers
│   │   ├── github_handler.py    # GitHub API integration
│   │   └── gemini_handler.py    # Gemini AI integration
│   ├── templates/         # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── assignment_detail.html
│   │   └── ...
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # App URLs
│   └── admin.py           # Admin configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── setup.sh              # Setup automation script
└── README.md             # This file
```

## 🗄️ Database Models

### Assignment
- Teacher (ForeignKey to User)
- Title
- Description
- Deadline
- Created/Updated timestamps

### StudentRepo
- Assignment (ForeignKey)
- Student name
- Repository URL
- GitHub data (commits, languages, README, etc.)
- AI analysis results
- Performance score
- Analysis status

### AnalysisLog
- Repository (ForeignKey)
- Analysis date
- Status (success/failed/pending)
- Error messages

## 🎯 Usage Guide

### 1. Register/Login
- Create an account or login with existing credentials
- Access the dashboard

### 2. Create Assignment
- Click "Create Assignment"
- Fill in title, description, and optional deadline
- Submit

### 3. Add Student Repositories

**Single Add:**
- Navigate to assignment detail
- Click "Add Repository"
- Enter student name and GitHub URL

**Bulk Add:**
- Click "Bulk Add Repositories"
- Enter data in format: `Student Name, GitHub URL`
- One entry per line

### 4. Analyze Repositories
- Click "Analyze" button next to any repository
- System will:
  - Fetch data from GitHub
  - Process with Gemini AI
  - Generate insights and score
  - Display results

### 5. View Results
- Click "View" to see detailed analysis
- Review AI summary, strengths, and recommendations
- Check performance score
- View language breakdown and commit history

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | Yes |
| `GITHUB_TOKEN` | GitHub API token | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### API Rate Limits

- **GitHub API:** 5,000 requests/hour (authenticated)
- **Gemini API:** Check your plan limits

## 🚀 Deployment

### Using Render/Railway/Vercel

1. Set environment variables in platform
2. Update `ALLOWED_HOSTS` in settings.py
3. Set `DEBUG=False`
4. Configure PostgreSQL database (optional)
5. Run migrations
6. Collect static files: `python manage.py collectstatic`

## 🧪 Testing

Run Django's built-in tests:
```bash
python manage.py test
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

MIT License © 2025

## 👨‍💻 Author

**Aadil Inamdar**
- AI & Web Developer
- Builder of GenAI and EdTech tools

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review API documentation:
  - [GitHub API](https://docs.github.com/rest)
  - [Gemini API](https://ai.google.dev/docs)

## 🔮 Future Enhancements

- [ ] Student login and personalized dashboards
- [ ] Plagiarism detection via AI
- [ ] Code quality metrics and static analysis
- [ ] GitHub OAuth integration
- [ ] Email/Telegram notifications
- [ ] PDF report generation
- [ ] Real-time collaboration features
- [ ] Mobile app support

---

**Built with ❤️ using Django, GitHub API & Gemini AI**
