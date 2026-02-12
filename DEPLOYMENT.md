# TuxHuz Deployment Guide

## Quick Start (Development)

### Windows

```bash
# 1. Navigate to backend
cd backend

# 2. Run setup script
setup.bat

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Start backend (in backend directory)
python -m flask run

# 5. In a new terminal, start frontend
cd Frontend
npm install
npm run dev
```

### Linux/macOS

```bash
# 1. Navigate to backend
cd backend

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run setup script
./setup.sh

# 4. Activate virtual environment
source venv/bin/activate

# 5. Start backend
python -m flask run

# 6. In a new terminal, start frontend
cd Frontend
npm install
npm run dev
```

## Configuration

### 1. Backend Configuration (.env file)

Create or update `backend/.env` with your settings:

```env
# Environment
FLASK_ENV=development
FLASK_DEBUG=False

# Security Keys (change these in production!)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Clash Royale API
CLASH_ROYALE_API_KEY=your-api-key-from-developer.clashroyale.com

# Database (for production with MySQL)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_db_user
MYSQL_PASSWORD=your_db_password
MYSQL_DATABASE=clash_royale_db

# CORS (for frontend)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Caching
PLAYER_CACHE_DURATION=300
CARDS_CACHE_DURATION=86400
```

### 2. Frontend Configuration (.env file)

Create `Frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

For production, change to your actual backend URL:
```env
VITE_API_BASE_URL=https://your-domain.com/api
```

## Getting Clash Royale API Key

1. Visit [developer.clashroyale.com](https://developer.clashroyale.com/)
2. Sign in with your Supercell ID
3. Create a new API Key
4. Add your server IP to the allowed IPs list
5. Copy the key and add to `.env` file

## Database Setup

### SQLite (Development - Default)
No setup needed! The app uses `clash_royale_dev.db` automatically.

### MySQL (Production)

```bash
# 1. Install MySQL Server
# Windows: Download from mysql.com
# Linux: sudo apt-get install mysql-server
# macOS: brew install mysql

# 2. Create database and user
mysql -u root -p

mysql> CREATE DATABASE clash_royale_db;
mysql> CREATE USER 'clash_royale_user'@'localhost' IDENTIFIED BY 'strong_password';
mysql> GRANT ALL PRIVILEGES ON clash_royale_db.* TO 'clash_royale_user'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> EXIT;

# 3. Update .env with MySQL credentials
FLASK_ENV=production
MYSQL_HOST=localhost
MYSQL_USER=clash_royale_user
MYSQL_PASSWORD=strong_password
MYSQL_DATABASE=clash_royale_db

# 4. Initialize database tables
# The app will auto-create tables on first run
```

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows or: source venv/bin/activate
python -m flask run
# Backend runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd Frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### Production Mode

#### Option 1: Gunicorn (Recommended)

```bash
cd backend
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Set production environment
export FLASK_ENV=production  # Windows: set FLASK_ENV=production

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Build and Serve Frontend from Backend

```bash
# 1. Build frontend
cd Frontend
npm run build
# Creates dist/ folder

# 2. Copy built files to backend
cp -r dist/* ../backend/static/
# Windows: copy dist to backend/static/

# 3. Run backend
cd ../backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
# Access on http://localhost:5000
```

## Docker Deployment (Optional)

Create `Dockerfile` in project root:

```dockerfile
# Backend stage
FROM python:3.11-slim as backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

# Frontend stage
FROM node:18-alpine as frontend
WORKDIR /app
COPY Frontend/package*.json .
RUN npm install
COPY Frontend .
RUN npm run build

# Final stage
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend .
COPY --from=frontend /app/dist ./static
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t tuxhuz .
docker run -p 5000:5000 -e CLASH_ROYALE_API_KEY=your_key tuxhuz
```

## Deployment Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env` to a random string
- [ ] Change `JWT_SECRET_KEY` to a random string
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure MySQL database
- [ ] Get Clash Royale API key and add to `.env`
- [ ] Update `CORS_ORIGINS` in `.env` to your domain
- [ ] Set `VITE_API_BASE_URL` in frontend `.env` to your backend URL
- [ ] Run `npm run build` for frontend
- [ ] Test with production server (gunicorn)
- [ ] Set up SSL/HTTPS (using nginx or similar)
- [ ] Configure firewall rules

## Troubleshooting

### API Key Issues
- Make sure IP address is added to Clash Royale API allowed IPs
- Check that API key is correct in `.env`

### Database Connection
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists

### CORS Errors
- Add your frontend URL to `CORS_ORIGINS` in `.env`
- For production, use your actual domain

### Frontend Build Issues
```bash
# Clear node_modules and reinstall
cd Frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Port Already in Use
```bash
# Change Flask port
python -m flask run --port 5001

# Change Vite port
npm run dev -- --port 5174
```

## Monitoring & Logs

### Flask Development Server
Logs are printed to console. For production, use:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile access.log --error-logfile error.log app:app
```

### Check Application Status
```bash
# Test backend
curl http://localhost:5000/health

# Test frontend
curl http://localhost:5173
```

## Support

For issues or questions:
1. Check the logs
2. Verify `.env` configuration
3. Ensure all dependencies are installed
4. Check that Clash Royale API key is valid

---

**Happy Deploying!** 🚀
