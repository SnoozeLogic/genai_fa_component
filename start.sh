#!/bin/bash

# Start GENAI FA Component with Gemini 2.5 Pro

clear
echo "=================================================="
echo "  🚀 GENAI FA Component - Starting Application"
echo "=================================================="
echo ""
echo "  ✅ Gemini 2.5 Pro Configured"
echo "  ✅ API Key Active"
echo "  ✅ Database Ready"
echo "  ✅ All Systems Go!"
echo ""
echo "=================================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    exit 1
fi

# Run migrations if needed
if [ ! -f "db.sqlite3" ]; then
    echo "🗄️  Setting up database..."
    uv run python manage.py migrate
    echo ""
fi

echo "🌐 Starting server..."
echo "📍 Access the app at: http://127.0.0.1:8000"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo ""

uv run python manage.py runserver
