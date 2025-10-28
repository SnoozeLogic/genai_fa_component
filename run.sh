#!/bin/bash

# Quick run script for GENAI FA Component (using uv)

echo "🚀 Starting GENAI FA Component..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Creating from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys before continuing!"
    exit 1
fi

# Run migrations if needed
if [ ! -f "db.sqlite3" ]; then
    echo "🗄️  Running migrations..."
    uv run python manage.py migrate
fi

# Start server
echo "🌐 Starting development server..."
echo "📍 Visit: http://127.0.0.1:8000"
echo ""

uv run python manage.py runserver
