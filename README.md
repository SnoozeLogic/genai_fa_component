Got it ✅ Aadil — here’s a **complete and well-documented `.md` (Markdown) project guide** for your **GenAI-powered Student Submission Tracker** using **Gemini API + GitHub API + Django (uv) + HTML Templates**.

You can directly save this as `README.md` or feed it to your CLI/agent for task automation and development setup.

---

````markdown
# 🚀 EduTrack AI — GenAI-Powered Student Submission Tracker

## 🧠 Overview

**EduTrack AI** is a GenAI-based project tracking system for educators.  
It automates student submission tracking by integrating **GitHub API** and **Gemini API**.

Teachers provide GitHub repository links of students.  
The system fetches data such as commits, languages, README content, and activity stats, then uses **Gemini API** to generate AI-based summaries, performance insights, and visual dashboards.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Frontend | HTML, CSS, Bootstrap/Tailwind, JavaScript |
| Backend | Django + Uvicorn (ASGI) |
| Database | PostgreSQL / SQLite |
| APIs | GitHub REST API, Gemini API |
| Visualization | Chart.js / Plotly |
| Hosting | Render / Railway / Azure |
| Version Control | Git & GitHub |

---

## ⚙️ System Workflow

```mermaid
flowchart TD
A[Teacher Login] --> B[Add Student GitHub Repo Links]
B --> C[Store Links in Database]
C --> D[Fetch Repo Data via GitHub API]
D --> E[Extract Commits, Code Stats, Readme, Languages]
E --> F[Send Data to Gemini API for Analysis]
F --> G[Receive AI Summary and Insights]
G --> H[Store Results in DB]
H --> I[Display Dashboard with Charts & Summaries]
I --> J[Generate PDF/Report for Teacher]
````

---

## 🧩 Features

### 👨‍🏫 Teacher Panel

* Login/Register functionality
* Add new assignments
* Submit list of student GitHub repo URLs
* View AI-generated insights for each student

### 🔍 GitHub Integration

* Fetch:

  * Total commits
  * Latest commit message & date
  * Languages used
  * README.md content
  * Contributors
* Data fetched using **GitHub REST API**

### 🧠 AI Integration (Gemini API)

* Use Gemini to analyze repository data
* Generate:

  * Code summary
  * Activity report
  * Performance insights
  * Suggestions for improvement

### 📊 Dashboard

* Visualize:

  * Commits per week
  * Top active students
  * Language usage graphs
* Display Gemini summary cards
* Option to export reports as PDF

---

## 🧱 System Architecture

**1. Frontend Layer**

* HTML Templates + Bootstrap
* Dynamic rendering with Django Context
* AJAX requests for live updates

**2. Backend Layer**

* Django views handle routing
* GitHub API requests handled via `requests` module
* Gemini API called via REST (JSON input/output)
* Data stored in local database

**3. AI Processing Layer**

* Data fetched from GitHub → converted to prompt
* Prompt sent to Gemini model
* Response parsed and stored as summary/insights

---

## 🧠 Example Gemini Prompt

```json
{
  "input": {
    "repo_summary": {
      "commits": 42,
      "languages": ["Python", "HTML", "CSS"],
      "readme_excerpt": "This project implements a Django-based blog system...",
      "recent_activity": "5 commits in last 7 days"
    },
    "instruction": "Summarize the student's progress, code quality, and give feedback in 150 words."
  }
}
```

**Expected Gemini Output:**

```json
{
  "summary": "The student has shown consistent progress with 42 commits and regular activity. The use of Django reflects good understanding of backend design. Code structure is modular and follows best practices. Further improvements can include better documentation and test coverage."
}
```

---

## 📦 API Integration

### 🔹 GitHub API (Example)

```python
import requests

def fetch_github_data(repo_url, token):
    repo_name = repo_url.split("github.com/")[-1]
    headers = {"Authorization": f"token {token}"}
    base_url = f"https://api.github.com/repos/{repo_name}"
    
    commits = requests.get(f"{base_url}/commits", headers=headers).json()
    langs = requests.get(f"{base_url}/languages", headers=headers).json()
    readme = requests.get(f"{base_url}/readme", headers=headers, params={"ref": "main"}).json()

    return {
        "commit_count": len(commits),
        "languages": list(langs.keys()),
        "readme_excerpt": readme.get("content", "")[:200]
    }
```

---

## 🧩 Django Structure

```
EduTrackAI/
├── manage.py
├── requirements.txt
├── edutrack/              # main Django app
│   ├── templates/
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   └── teacher_panel.html
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── api/
│       ├── github_handler.py
│       └── gemini_handler.py
└── db.sqlite3
```

---

## 🗄️ Database Models (Example)

```python
from django.db import models

class StudentRepo(models.Model):
    name = models.CharField(max_length=100)
    repo_url = models.URLField()
    commit_count = models.IntegerField(default=0)
    languages = models.JSONField(default=list)
    last_updated = models.DateTimeField(auto_now=True)
    ai_summary = models.TextField(blank=True, null=True)

class Assignment(models.Model):
    teacher_name = models.CharField(max_length=100)
    assignment_title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
GITHUB_TOKEN=<your_github_token>
GEMINI_API_KEY=<your_gemini_api_key>
DEBUG=True
```

Load them in `settings.py` using `python-dotenv`.

---

## ⚡ Installation Guide

```bash
# Clone repository
git clone https://github.com/yourname/edutrack-ai.git
cd edutrack-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server with uvicorn
uvicorn edutrack.asgi:application --reload
```

---

## 🧠 Future Enhancements

* Add student login to view personalized feedback
* Integrate plagiarism detection (via Gemini)
* Add code quality scoring using static analysis
* Enable GitHub OAuth instead of manual repo link entry
* Add notifications (email or Telegram bot)

---

## 📜 License

MIT License © 2025 [Aadil Inamdar]

---

## 👨‍💻 Author

**Aadil Inamdar**
AI & Web Developer | Builder of GenAI and EdTech tools
📧 [[aadil@example.com](mailto:aadil@example.com)]
🌐 [Portfolio / Website Link]

```

---

Would you like me to also generate the **`requirements.txt`** and **basic Django folder scaffolding (with working sample code)** next? That would make it directly executable for your CLI agent.
```
