#!/bin/bash

# EduTrack AI - Setup and Run Script (using uv)

echo "=========================================="
echo "  EduTrack AI - GenAI Student Tracker"
echo "=========================================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install uv"
        exit 1
    fi
    
    echo "✅ uv installed successfully"
    echo "⚠️  Please restart your shell and run this script again"
    exit 0
fi

echo "✅ uv found: $(uv --version)"
echo ""

# Sync dependencies using uv
echo "📥 Syncing dependencies with uv..."
uv sync

if [ $? -ne 0 ]; then
    echo "❌ Failed to sync dependencies"
    exit 1
fi

echo "✅ Dependencies synced"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   - GITHUB_TOKEN"
    echo "   - GEMINI_API_KEY"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Make migrations
echo "🗄️  Creating database migrations..."
uv run python manage.py makemigrations

# Run migrations
echo "🗄️  Running database migrations..."
uv run python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Migration failed"
    exit 1
fi

echo "✅ Database setup complete"
echo ""

# Create superuser prompt
echo "👤 Do you want to create a superuser account? (y/n)"
read -r create_superuser

if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    uv run python manage.py createsuperuser
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  uv run python manage.py runserver"
echo ""
echo "Or use uvicorn (ASGI):"
echo "  uv run uvicorn config.asgi:application --reload"
echo ""
echo "Then visit: http://127.0.0.1:8000"
echo ""
echo "💡 Useful uv commands:"
echo "  uv sync           - Sync dependencies"
echo "  uv add <package>  - Add a new package"
echo "  uv run <command>  - Run command in uv environment"
echo ""
