#!/usr/bin/env python
"""
Local Render Deployment Simulator
Simulates the Render environment locally with gunicorn
"""
import os
import sys
import subprocess
import platform

def setup_production_env():
    """Set up production environment variables"""
    env_vars = {
        'FLASK_ENV': 'production',
        'FLASK_DEBUG': 'False',
        'SECRET_KEY': os.getenv('SECRET_KEY', 'render-secret-key-change-me'),
        'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY', 'render-jwt-secret-key-change-me'),
        'CLASH_ROYALE_API_KEY': os.getenv('CLASH_ROYALE_API_KEY', ''),
        'CORS_ORIGINS': 'http://localhost:3000,http://localhost:5173,http://localhost:5174',
        'PORT': '5000'
    }
    
    return env_vars

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    cmd = [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']
    result = subprocess.run(cmd, cwd='backend')
    if result.returncode != 0:
        print("❌ Failed to install dependencies")
        sys.exit(1)
    print("✅ Dependencies installed")

def run_backend_production():
    """Run backend with gunicorn (production mode)"""
    print("\n🚀 Starting backend in production mode with gunicorn...")
    print("💡 This simulates the Render environment locally")
    print("📍 Backend URL: http://localhost:5000")
    print("📍 API URL: http://localhost:5000/api")
    print("\nPress Ctrl+C to stop\n")
    
    env = os.environ.copy()
    env_vars = setup_production_env()
    env.update(env_vars)
    
    # On Windows, gunicorn has issues with certain workers
    # Use sync worker which is more compatible
    cmd = [
        sys.executable, '-m', 'gunicorn',
        '-w', '2',
        '-b', '0.0.0.0:5000',
        '--worker-class', 'sync',
        '--access-logfile', '-',
        '--error-logfile', '-',
        'wsgi:app'
    ]
    
    try:
        subprocess.run(cmd, cwd='backend', env=env)
    except KeyboardInterrupt:
        print("\n\n✋ Backend stopped")
        sys.exit(0)

def run_backend_development():
    """Run backend in development mode with Flask"""
    print("\n🚀 Starting backend in development mode with Flask...")
    print("📍 Backend URL: http://localhost:5000")
    print("📍 API URL: http://localhost:5000/api")
    print("\nPress Ctrl+C to stop\n")
    
    env = os.environ.copy()
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = 'True'
    
    cmd = [sys.executable, '-m', 'flask', 'run']
    
    try:
        subprocess.run(cmd, cwd='backend', env=env)
    except KeyboardInterrupt:
        print("\n\n✋ Backend stopped")
        sys.exit(0)

def check_gunicorn():
    """Check if gunicorn is installed"""
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'show', 'gunicorn'],
        capture_output=True
    )
    return result.returncode == 0

def main():
    """Main function"""
    print("=" * 60)
    print("🎯 Local Render Deployment Simulator")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('backend'):
        print("❌ Error: 'backend' directory not found")
        print("Run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Check gunicorn
    if not check_gunicorn():
        print("⚠️  gunicorn not installed")
        print("Installing gunicorn...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'gunicorn'])
    
    # Ask user for deployment mode
    print("\n" + "=" * 60)
    print("Choose deployment mode:")
    print("=" * 60)
    print("1️⃣  Production mode (gunicorn - like Render)")
    print("2️⃣  Development mode (Flask dev server)")
    print("3️⃣  Exit")
    print("")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == '1':
        run_backend_production()
    elif choice == '2':
        run_backend_development()
    elif choice == '3':
        print("👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice")
        sys.exit(1)

if __name__ == '__main__':
    main()
