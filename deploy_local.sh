#!/bin/bash

# Local Render Deployment Simulator for Linux/macOS
# This script simulates the Render production environment locally

set -u

echo ""
echo "============================================================"
echo ""
echo "  🚀  Local Render Deployment Simulator"
echo ""
echo "============================================================"
echo ""

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Error: 'backend' directory not found"
    echo "Run this script from the project root directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
cd backend
python3 -m pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed!"
cd ..

# Check gunicorn
echo "⏳ Checking gunicorn..."
python3 -m pip show gunicorn >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "📦 Installing gunicorn..."
    python3 -m pip install gunicorn -q
fi

echo ""
echo "============================================================"
echo "Choose deployment mode:"
echo "============================================================"
echo "1️⃣  Production mode (gunicorn - like Render)"
echo "2️⃣  Development mode (Flask dev server)"
echo "3️⃣  Exit"
echo ""
read -p "Enter your choice (1/2/3): " choice

case "$choice" in
    1)
        echo ""
        echo "🚀 Launching backend in PRODUCTION mode with gunicorn..."
        echo "   Configure: http://localhost:5000"
        echo "   API: http://localhost:5000/api"
        echo ""
        echo "Press Ctrl+C to stop"
        echo ""
        cd backend
        export FLASK_ENV=production
        export FLASK_DEBUG=False
        export PORT=5000
        python3 -m gunicorn -w 4 -b 0.0.0.0:5000 --reload --access-logfile - --error-logfile - wsgi:app
        cd ..
        ;;
    2)
        echo ""
        echo "🚀 Launching backend in DEVELOPMENT mode with Flask..."
        echo "   Configure: http://localhost:5000"
        echo "   API: http://localhost:5000/api"
        echo ""
        echo "Press Ctrl+C to stop"
        echo ""
        cd backend
        export FLASK_ENV=development
        export FLASK_DEBUG=True
        python3 -m flask run
        cd ..
        ;;
    3)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
