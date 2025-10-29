# 🎓 GENAI FA Component

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Gemini AI](https://img.shields.io/badge/Gemini-2.5_Pro-orange?style=for-the-badge&logo=google)
![GitHub API](https://img.shields.io/badge/GitHub-API-black?style=for-the-badge&logo=github)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**AI-Powered Student Repository Analysis & Tracking System**

Track student GitHub repositories, analyze code quality, and generate AI-powered insights with Google's Gemini 2.5 Pro.

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Screenshots](#-screenshots)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Integration](#-api-integration)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🌟 Overview

**GENAI FA Component** is a comprehensive GenAI-powered platform designed for educators to efficiently track, analyze, and provide feedback on student GitHub repositories. Built with Django and powered by Google's Gemini 2.5 Pro AI, it automates the tedious process of code review and provides actionable insights.

### Why GENAI FA Component?

- ✅ **Automated Analysis**: AI-powered code review using Gemini 2.5 Pro
- ✅ **Bulk Operations**: Upload multiple repositories via CSV
- ✅ **Comprehensive Metrics**: Track commits, languages, contributors, and more
- ✅ **Performance Scoring**: AI-generated scores (0-100) with detailed feedback
- ✅ **Beautiful Dashboard**: Modern UI with statistics and analytics
- ✅ **GitHub Integration**: Seamless repository data fetching
- ✅ **No Token Required**: Works with public repositories without GitHub token

---

## 🚀 Features

### 🎯 Core Features

#### 1. **Assignment Management**
- Create unlimited assignments with titles, descriptions, and deadlines
- Set custom deadlines with date/time picker
- Track multiple assignments simultaneously
- View assignment analytics and statistics

#### 2. **Repository Tracking**
- **Single Add**: Add repositories one at a time with student name
- **Bulk Upload**: CSV upload for multiple repositories
  ```csv
  Student Name, Repository URL
  John Doe, https://github.com/johndoe/project
  Jane Smith, https://github.com/janesmith/app
  ```
- Support for both public and private repositories
- Automatic repository validation

#### 3. **AI-Powered Analysis** 🤖
Powered by **Google Gemini 2.5 Pro**, the analysis includes:
- **Summary**: Comprehensive project overview (50-75 words)
- **Strengths**: 3-5 positive aspects identified
- **Areas for Improvement**: 3-5 specific suggestions
- **Performance Score**: 0-100 rating based on:
  - Code activity and commit frequency
  - Documentation quality
  - Best practices and code organization
  - Project completeness
- **Recommendations**: 2-3 actionable next steps

#### 4. **GitHub Data Extraction**
Automatically fetches:
- 📊 **Commit History**: Total commits with messages and dates
- 💻 **Programming Languages**: Language breakdown with percentages
- 👥 **Contributors**: List of all contributors with GitHub profiles
- 📝 **README Content**: Full README for context
- 📅 **Last Commit**: Most recent commit details
- 🏷️ **Repository Info**: Description, stars, forks

#### 5. **Beautiful Dashboard**
- **Assignment Cards**: Visual cards showing:
  - Student count
  - Deadline status (color-coded)
  - Analysis progress with progress bars
  - Quick action buttons
- **Statistics Overview**:
  - Total students per assignment
  - Analyzed vs. pending repositories
  - Average performance scores
  - Total commits across all repos
- **Color-Coded Status**:
  - 🔴 Red: Deadline passed
  - 🟠 Orange: Deadline approaching (within 7 days)
  - 🟢 Green: Deadline in future

#### 6. **Assignment Detail View**
Comprehensive statistics display:
- 📊 **Total Students**: Number of repositories submitted
- 📝 **Total Commits**: Aggregate commit count
- 💻 **Languages Used**: Unique programming languages count
- ⏺️ **Analysis Progress**: Circular progress indicator
- 📈 **Average Score**: Mean performance score
- 🏆 **Top Performers**: Leaderboard of highest scores
- 📉 **Score Range**: Min-max score display

#### 7. **Repository Detail Page**
Individual repository analysis showing:
- **Statistics Cards**:
  - Commit count
  - Languages used (with percentages)
  - Contributors count
  - AI performance score
- **AI Analysis** (Markdown formatted):
  - Full summary
  - Strengths list
  - Improvements needed
  - Recommendations
- **Contributors Section**:
  - Profile pictures
  - Clickable GitHub profiles
- **Language Breakdown**: Visual representation with colors

#### 8. **Analytics Dashboard** 📊
- Total repositories tracked
- Total students enrolled
- Overall analysis completion rate
- Average performance score across all assignments
- Commit activity trends
- Language usage statistics
- Top performing students

### 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Bootstrap 5**: Modern, clean interface
- **Gradient Cards**: Beautiful purple/indigo color scheme
- **Bootstrap Icons**: Comprehensive icon set
- **Progress Indicators**: Visual feedback for all operations
- **Markdown Rendering**: Properly formatted AI analysis
- **Status Badges**: Color-coded indicators
- **Hover Effects**: Interactive elements with smooth transitions
- **Loading States**: AJAX-based operations with spinners

---

## 🛠️ Tech Stack

### Backend
- **Django 5.2.7**: Web framework
- **Python 3.10+**: Programming language
- **SQLite**: Database (development)
- **Uvicorn**: ASGI server
- **uv**: Ultra-fast package manager

### Frontend
- **Bootstrap 5**: CSS framework
- **Bootstrap Icons**: Icon library
- **JavaScript (Vanilla)**: Client-side interactions
- **AJAX**: Asynchronous requests

### APIs
- **Google Gemini 2.5 Pro**: AI analysis
- **GitHub REST API v3**: Repository data

### Tools
- **Git**: Version control
- **uv**: Dependency management
- **Markdown**: Text formatting

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│         (Bootstrap 5 + JavaScript + AJAX)                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Django Backend                          │
│  ┌──────────────┬──────────────┬──────────────────┐    │
│  │   Views      │    Models    │   Template Tags  │    │
│  │              │              │                   │    │
│  │  - Dashboard │  - Assignment│  - Markdown      │    │
│  │  - Analytics │  - StudentRepo│    Filter       │    │
│  │  - API Views │  - AnalysisLog│                 │    │
│  └──────┬───────┴──────┬───────┴──────────────────┘    │
│         │              │                                 │
│  ┌──────▼──────┐  ┌───▼──────┐                         │
│  │   API       │  │ Database  │                         │
│  │ Handlers    │  │ (SQLite)  │                         │
│  └──────┬──────┘  └───────────┘                         │
└─────────┼──────────────────────────────────────────────┘
          │
    ┌─────▼─────┬──────────────┐
    │           │              │
┌───▼──────┐ ┌──▼────────┐ ┌──▼──────┐
│ Gemini   │ │  GitHub   │ │  User   │
│ 2.5 Pro  │ │    API    │ │  Auth   │
└──────────┘ └───────────┘ └─────────┘
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- GitHub Token (optional, for private repos)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SnoozeLogic/genai_fa_component.git
   cd genai_fa_component
   ```

2. **Install uv (if not installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Sync Dependencies**
   ```bash
   uv sync
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Add your API keys
   ```

   Required:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   Optional (for private repos):
   ```env
   GITHUB_TOKEN=your_github_token_here
   ```

5. **Run Database Migrations**
   ```bash
   uv run python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   uv run python manage.py createsuperuser
   ```

7. **Start the Server**
   ```bash
   ./start.sh
   ```
   Or manually:
   ```bash
   uv run python manage.py runserver
   ```

8. **Access the Application**
   ```
   http://127.0.0.1:8000
   ```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_django_secret_key_here

# Optional
GITHUB_TOKEN=your_github_token_here  # Only for private repos
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

#### GitHub Personal Access Token (Optional)
1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name: "GENAI FA Component"
4. Select scope: `repo` (Full control of private repositories)
5. Click "Generate token"
6. Copy the token to your `.env` file

**Note**: GitHub token is only needed for private repositories. Public repos work without a token.

---

## 📖 Usage

### 1. Create an Assignment

1. Log in to the dashboard
2. Click "Create New Assignment"
3. Fill in:
   - **Title**: Assignment name
   - **Description**: Assignment details
   - **Deadline**: Due date and time
4. Click "Create Assignment"

### 2. Add Student Repositories

#### Option A: Single Add
1. Open the assignment
2. Click "Add Repository"
3. Enter:
   - Student name
   - GitHub repository URL
4. Click "Add"

#### Option B: Bulk Upload
1. Open the assignment
2. Click "Bulk Upload"
3. Prepare CSV file:
   ```csv
   Student Name, Repository URL
   Alice Johnson, https://github.com/alice/project1
   Bob Smith, https://github.com/bob/project2
   ```
4. Upload the file
5. Review and confirm

### 3. Analyze Repositories

1. Click the "Analyze" button next to a repository
2. Wait for the AI analysis (10-30 seconds)
3. View the results:
   - Performance score
   - Detailed analysis
   - Strengths and improvements
   - Recommendations

### 4. View Analytics

- **Dashboard**: Overview of all assignments
- **Assignment Detail**: Statistics for specific assignment
- **Repository Detail**: Individual analysis results
- **Analytics Page**: Comprehensive metrics and trends

---

## 🔌 API Integration

### Gemini AI Handler

```python
from edutrack.api.gemini_handler import GeminiHandler

# Initialize handler
gemini = GeminiHandler()

# Analyze repository
result = gemini.analyze_repository(github_data)

# Extract analysis
analysis = result.get('analysis', {})
score = analysis.get('score')  # 0-100
summary = analysis.get('summary')
strengths = analysis.get('strengths')  # List
improvements = analysis.get('improvements')  # List
```

### GitHub Handler

```python
from edutrack.api.github_handler import GitHubHandler

# Initialize handler
github = GitHubHandler()

# Fetch repository data
data = github.fetch_repository_data('username/repo')

# Access data
commits = data.get('commits', [])
languages = data.get('languages', {})
contributors = data.get('contributors', [])
readme = data.get('readme', '')
```

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/dashboard.png)
*Modern dashboard with assignment cards and statistics*

### Assignment Detail
![Assignment Detail](docs/assignment_detail.png)
*Comprehensive view with statistics and student repositories*

### Repository Analysis
![Repository Analysis](docs/repo_analysis.png)
*AI-powered analysis with scores and recommendations*

### Analytics
![Analytics](docs/analytics.png)
*Detailed analytics and performance metrics*

---

## 📁 Project Structure

```
genai_fa_component/
├── config/                    # Django configuration
│   ├── settings.py           # Project settings
│   ├── urls.py               # URL routing
│   ├── asgi.py              # ASGI config
│   └── wsgi.py              # WSGI config
│
├── edutrack/                 # Main application
│   ├── api/                 # API integrations
│   │   ├── gemini_handler.py   # Gemini AI client
│   │   └── github_handler.py   # GitHub API client
│   │
│   ├── templates/           # HTML templates
│   │   ├── base.html           # Base layout
│   │   ├── dashboard.html      # Main dashboard
│   │   ├── assignment_detail.html
│   │   ├── repo_detail.html
│   │   └── ...
│   │
│   ├── templatetags/        # Custom template filters
│   │   └── markdown_filters.py
│   │
│   ├── static/              # Static files
│   │   ├── css/
│   │   └── js/
│   │
│   ├── migrations/          # Database migrations
│   ├── models.py            # Data models
│   ├── views.py             # View controllers
│   ├── urls.py              # App URL patterns
│   └── admin.py             # Admin panel
│
├── docs/                     # Documentation
│   ├── SETUP_COMPLETE.md
│   ├── SCORE_AND_STATS_FIX.md
│   ├── BRANDING_UPDATE.md
│   └── screenshots/
│
├── .env                      # Environment variables
├── .env.example             # Environment template
├── manage.py                # Django management
├── pyproject.toml           # uv configuration
├── uv.lock                  # Dependency lock
├── requirements.txt         # Python dependencies
├── start.sh                 # Startup script
├── run.sh                   # Quick run script
└── README.md                # This file
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run python manage.py test

# Check code style
uv run black .
uv run flake8

# Run migrations
uv run python manage.py makemigrations
uv run python manage.py migrate
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uv run python manage.py runserver 8080
```

#### 2. Gemini API Key Not Working
- Verify key is correct in `.env`
- Check API quota at [Google AI Studio](https://makersuite.google.com)
- Ensure you're using the correct model (gemini-2.5-pro)

#### 3. GitHub API Rate Limit
- Add a GitHub token to `.env`
- Token increases rate limit from 60 to 5000 requests/hour

#### 4. Score Not Extracting
- Check terminal for `[SCORE DEBUG]` messages
- Ensure Gemini response includes score in format: `85/100` or `Score: 85`
- Try re-analyzing the repository

#### 5. Dependencies Not Installing
```bash
# Clear cache and reinstall
rm -rf .venv uv.lock
uv sync
```

#### 6. Database Issues
```bash
# Reset database
rm db.sqlite3
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

### Debug Mode

Enable detailed logging:
```python
# config/settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## 📊 Performance

### Benchmarks
- **Analysis Time**: 10-30 seconds per repository
- **GitHub API**: <1 second for public repos
- **Dashboard Load**: <500ms
- **Bulk Upload**: ~1 second per 10 repositories

### Optimization Tips
1. Use GitHub token to avoid rate limits
2. Enable caching for repeated API calls
3. Use indexes on database queries
4. Implement pagination for large datasets

---

## 🔒 Security

- ✅ CSRF protection enabled
- ✅ Session-based authentication
- ✅ Environment variable configuration
- ✅ SQL injection protection (Django ORM)
- ✅ XSS protection
- ✅ Secure password hashing

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY`
- [ ] Add domain to `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure static file serving
- [ ] Set up backup strategy

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

## 🌟 Acknowledgments

- **Django Team**: For the amazing web framework
- **Google AI**: For Gemini 2.5 Pro API
- **GitHub**: For the comprehensive API
- **Bootstrap**: For the beautiful UI components
- **Astral**: For the uv package manager

---

## 📞 Support

- **Documentation**: See `/docs` folder
- **Issues**: [GitHub Issues](https://github.com/SnoozeLogic/genai_fa_component/issues)
- **Email**: support@genaifa.example.com

---

## 🗺️ Roadmap

### Team:

- **Aadil Inamdar: 65**
- **Siddhi Gurav: 44**
- **Adarsh pilavare: 50**


---

<div align="center">

**Made with ❤️ for educators and students**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/SnoozeLogic/genai_fa_component/issues) • [Request Feature](https://github.com/SnoozeLogic/genai_fa_component/issues)

</div>
