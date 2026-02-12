# Deploy TuxHuz Locally - Quick Reference

## ⚡ Fastest Way (Windows)

```batch
cd c:\Users\DELL\Desktop\TuxHuz
deploy_local.bat
```

Then select **Option 2** (Development mode - Flask)

## ⚡ Fastest Way (Linux/macOS)

```bash
cd ~/path/to/TuxHuz
chmod +x deploy_local.sh
./deploy_local.sh
```

Then select **Option 2** (Development mode - Flask)

## 🚀 Manually Start Backend (All Platforms)

### Development Mode (Recommended for Testing)

```bash
cd backend
set FLASK_ENV=development
set FLASK_DEBUG=True
python -m flask run
```

**Output should be:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Production Mode (Like Render)

```bash
cd backend
set FLASK_ENV=production
set FLASK_DEBUG=False
python -m gunicorn -w 2 --worker-class sync -b 0.0.0.0:5000 wsgi:app
```

## ✅ Test Your Backend

Open a new terminal and run:

```bash
# Health check
curl http://localhost:5000/

# Get cards (requires valid API key)
curl http://localhost:5000/api/cards

# Get players (requires valid API key)
curl http://localhost:5000/api/players
```

**Expected response:**
```json
{
  "message": "Clash Royale Deck Analyzer API",
  "version": "1.0.0",
  "endpoints": {
    "auth": "/api/auth",
    "cards": "/api/cards",
    "players": "/api/players",
    "roast": "/api/roast"
  }
}
```

## 🔧 Configuration

### Backend Environment Variables (backend/.env)

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key
JWT_SECRET_KEY=dev-jwt-secret
CLASH_ROYALE_API_KEY=your-api-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174
```

### Frontend (if needed)

```bash
cd Frontend
npm install
npm run dev
```

Then create `Frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

Frontend will run on: **http://localhost:5173**

## 📋 Deployment Modes Comparison

| Aspect | Development | Production (Gunicorn) |
|--------|-------------|----------------------|
| **Start Command** | `flask run` | `gunicorn` |
| **Hot Reload** | ✅ Yes | ❌ No |
| **Performance** | Lower | Higher |
| **Debugging** | ✅ Easy | Harder |
| **Matches Render** | ❌ No | ✅ Yes |
| **Recommended for** | Development | Testing Render |

## 🐛 Troubleshooting

### Port 5000 is Already in Use

```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or run on different port
set PORT=5001
```

### Backend won't start

1. Check you're in the correct directory:
   ```bash
   # ✅ Correct
   cd backend
   python -m flask run
   
   # ❌ Wrong
   python -m flask run  # (from root directory)
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Delete cache:
   ```bash
   rm -r __pycache__ .pytest_cache
   ```

### API Key not working

1. Go to [https://developer.clashroyale.com/](https://developer.clashroyale.com/)
2. Create a **NEW** API key
3. Leave "Allowed IP addresses" **BLANK**
4. Update `backend/.env`:
   ```env
   CLASH_ROYALE_API_KEY=your-new-key
   ```

### CORS errors

Update `backend/.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174
```

Then restart backend.

## 🔗 Useful URLs

| Service | URL |
|---------|-----|
| Backend API | http://localhost:5000 |
| Cards API | http://localhost:5000/api/cards |
| Players API | http://localhost:5000/api/players |
| Roast API | http://localhost:5000/api/roast |
| Frontend | http://localhost:5173 |

## 📦 File Structure

```
TuxHuz/
├── backend/
│   ├── app.py          ← Main Flask app
│   ├── wsgi.py         ← WSGI entry point (for gunicorn)
│   ├── config.py       ← Configuration
│   ├── requirements.txt ← Python dependencies
│   └── .env            ← Environment variables
├── Frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── .env
├── deploy_local.py     ← Local deployment script
├── deploy_local.bat    ← Windows batch script
├── deploy_local.sh     ← Linux/macOS script
├── LOCAL_DEPLOYMENT.md ← Detailed guide
└── RENDER_DEPLOYMENT.md ← Render deployment guide
```

## 🎯 Next Steps

1. **Test locally** - Run `deploy_local.bat` or `./deploy_local.sh`
2. **Verify API works** - Test endpoints with curl
3. **Check logs** - Look for errors in terminal
4. **Push to GitHub** - When ready to deploy
5. **Deploy to Render** - Use Render Dashboard

## 📚 Complete Guides

- **[LOCAL_DEPLOYMENT.md](LOCAL_DEPLOYMENT.md)** - Detailed local deployment guide
- **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** - Detailed Render deployment guide
- **[RENDER_QUICK_START.md](RENDER_QUICK_START.md)** - Quick Render setup

## 💻 Commands Cheat Sheet

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start backend (development)
cd backend && python -m flask run

# Start backend (production/gunicorn)
cd backend && python -m gunicorn -w 2 --worker-class sync -b 0.0.0.0:5000 wsgi:app

# Test API
curl http://localhost:5000/

# Start frontend
cd Frontend && npm install && npm run dev

# Check if port is in use
netstat -ano | findstr :5000

# View logs
tail -f backend/runserver.log
```

---

✅ **Your deployment is ready!** Choose your preferred method above and start testing.
