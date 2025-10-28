# EduTrack AI - Quick Start Guide (Using uv)

## Prerequisites
- Python 3.8 or higher
- uv package manager

## Installation

### 1. Install uv (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup
```bash
cd genai_fa_component
./setup.sh
```

### 3. Configure Environment Variables
Edit `.env` file and add your API keys:
```bash
GITHUB_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
```bash
./run.sh
```

Or manually:
```bash
uv run python manage.py runserver
```

## Common uv Commands

### Sync dependencies
```bash
uv sync
```

### Add a new package
```bash
uv add package-name
```

### Remove a package
```bash
uv remove package-name
```

### Run Django commands
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

### Run with uvicorn (ASGI)
```bash
uv run uvicorn config.asgi:application --reload
```

### Run tests
```bash
uv run python manage.py test
```

### Add development dependencies
```bash
uv add --dev pytest black flake8
```

## Project Structure
```
genai_fa_component/
├── pyproject.toml          # Project configuration & dependencies (uv)
├── uv.lock                 # Lock file (auto-generated)
├── setup.sh                # Setup script (using uv)
├── run.sh                  # Quick run script
├── manage.py               # Django management
├── config/                 # Django settings
├── edutrack/               # Main app
│   ├── api/               # API handlers
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models
│   └── views.py           # View logic
├── .env.example           # Environment template
└── README.md              # Documentation
```

## Why uv?

- ⚡ **10-100x faster** than pip
- 🔒 **Deterministic** dependency resolution
- 📦 **All-in-one** tool (replaces pip, pip-tools, virtualenv)
- 🚀 **Modern** and actively maintained
- 💾 **Disk space efficient** with global cache

## Next Steps

1. Visit http://127.0.0.1:8000
2. Register a new account
3. Create an assignment
4. Add student GitHub repositories
5. Analyze repositories with AI

## Getting API Keys

- **GitHub Token:** https://github.com/settings/tokens (needs `repo` scope)
- **Gemini API Key:** https://makersuite.google.com/app/apikey

## Troubleshooting

### Sync failed?
```bash
rm -rf .venv uv.lock
uv sync
```

### Import errors?
```bash
uv sync --refresh
```

### Database issues?
```bash
rm db.sqlite3
uv run python manage.py migrate
```
