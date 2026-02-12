# TuxHuz - Deployment Ready ✅

## Quick Start Guide

### 1️⃣ **Option A: Local Development (Recommended for testing)**

**Windows:**
```bash
cd backend
setup.bat
# Then in separate terminals:
# Terminal 1: python -m flask run
# Terminal 2: cd Frontend && npm install && npm run dev
```

**Linux/macOS:**
```bash
cd backend
chmod +x setup.sh
./setup.sh
# Then in separate terminals:
# Terminal 1: source venv/bin/activate && python -m flask run
# Terminal 2: cd Frontend && npm install && npm run dev
```

### 2️⃣ **Option B: Docker Deployment (All-in-one)**

```bash
# Copy .env.example to .env and configure
cp .env.example backend/.env

# Start all services
docker-compose up --build

# Access:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:5000
# - API: http://localhost:5000/api
# - MySQL: localhost:3306
```

### 3️⃣ **Option C: Production Deployment**

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed production setup.

---

## 🔧 Configuration Checklist

Before running, ensure:

- [ ] **Clash Royale API Key** - Get from [developer.clashroyale.com](https://developer.clashroyale.com/)
  - Add to `backend/.env`: `CLASH_ROYALE_API_KEY=your_key`
  - Add your server IP to API's allowed IPs list

- [ ] **Database** (for MySQL)
  - Update `backend/.env` with MySQL credentials
  - Or use SQLite (default in development)

- [ ] **Environment Variables**
  - Backend: `backend/.env`
  - Frontend: `Frontend/.env`
  - See `.env.example` for template

---

## 📁 Project Structure

```
TuxHuz/
├── backend/               # Flask API Server
│   ├── requirements.txt   # Python dependencies
│   ├── app.py             # Main Flask app
│   ├── config.py          # Configuration
│   ├── models.py          # Database models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   ├── .env               # Environment variables
│   └── Dockerfile         # Docker config
├── Frontend/              # React SPA
│   ├── package.json       # Node dependencies
│   ├── src/               # React components
│   ├── .env               # Environment variables
│   └── Dockerfile         # Docker config
├── docker-compose.yml     # Complete stack
├── DEPLOYMENT.md          # Full deployment guide
└── README.md              # Project info
```

---

## 🚀 What's Included

✅ Full-stack Flask + React application
✅ Clash Royale API integration
✅ Database models (SQLite/MySQL)
✅ Authentication system (JWT)
✅ Deck analysis engine
✅ Player statistics tracking
✅ Card database
✅ API documentation
✅ Docker support
✅ Deployment scripts
✅ Error handling
✅ CORS configuration

---

## 🔗 Important URLs

- **Frontend Dev**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Docs**: http://localhost:5000/ (root endpoint)
- **Database**: sqlite:///clash_royale_dev.db (SQLite) or MySQL (production)

---

## 📝 Environmental Variables

Key variables in `.env`:

```env
# Security
FLASK_ENV=development
SECRET_KEY=your-secret
JWT_SECRET_KEY=your-jwt-secret

# API
CLASH_ROYALE_API_KEY=your-api-key

# Database
MYSQL_HOST=localhost
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_DATABASE=database

# CORS
CORS_ORIGINS=http://localhost:5173

# Frontend
VITE_API_BASE_URL=http://localhost:5000/api
```

---

## ⚠️ Common Issues & Solutions

**Port in use?**
```bash
# Change port: python -m flask run --port 5001
```

**Database errors?**
```bash
# Reinitialize: python init_db.py
```

**Module not found?**
```bash
# Backend: pip install -r requirements.txt
# Frontend: npm install
```

**API not responding?**
- Check Clash Royale API key in `.env`
- Verify CORS configuration
- Check backend logs

---

## 📚 Documentation

- Full setup: [DEPLOYMENT.md](./DEPLOYMENT.md)
- API endpoints: See `backend/routes/`
- Frontend components: See `Frontend/src/`
- Database schema: See `backend/models.py`

---

## 🎯 Next Steps

1. **Configure API Key**: Add Clash Royale API key to `.env`
2. **Choose Deployment**: Local, Docker, or Production
3. **Start Services**: Run backend and frontend
4. **Test**: Visit `http://localhost:5173`
5. **Deploy**: Follow [DEPLOYMENT.md](./DEPLOYMENT.md)

---

**You're ready to deploy!** 🎉

For detailed instructions, see `DEPLOYMENT.md`
