# Local Render Deployment Guide

Deploy and test your TuxHuz application locally using the same production environment as Render.

## Quick Start

### Windows Users

```bash
# Run the deployment script
deploy_local.bat
```

Then select **Option 1** for production mode (gunicorn) or **Option 2** for development mode.

### Linux/macOS Users

```bash
# Make the script executable
chmod +x deploy_local.sh

# Run the deployment script
./deploy_local.sh
```

Then select **Option 1** for production mode (gunicorn) or **Option 2** for development mode.

### Python Script (All Platforms)

```bash
python deploy_local.py
```

## What Gets Deployed

### Mode 1: Production (Gunicorn - Like Render)
This mode simulates the **exact Render environment** locally:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

- Uses the `wsgi:app` entry point (same as on Render)
- Runs with 4 workers (same as on Render)
- No hot-reload by default, but we enable `--reload` for development
- Simulates production performance

**Environment Variables (Production):**
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=render-secret-key-change-me
JWT_SECRET_KEY=render-jwt-secret-key-change-me
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174
PORT=5000
```

### Mode 2: Development (Flask Dev Server)
This mode uses Flask's built-in development server:

```bash
flask run
```

- Hot-reloads on code changes
- Easier debugging
- Development-friendly error messages
- Auto-reloads templates and static files

**Environment Variables (Development):**
```
FLASK_ENV=development
FLASK_DEBUG=True
```

## Accessing Your Application

Once deployed, access your backend at:

- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/
- **Players API**: http://localhost:5000/api/players
- **Cards API**: http://localhost:5000/api/cards
- **Roast API**: http://localhost:5000/api/roast

## Testing the Backend

### 1. Health Check

```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "message": "Clash Royale Deck Analyzer API",
  "version": "1.0.0",
  "endpoints": {
    "auth": "/api/auth",
    "players": "/api/players",
    "cards": "/api/cards",
    "roast": "/api/roast"
  }
}
```

### 2. Get Cards (Requires Valid API Key)

Make sure your `CLASH_ROYALE_API_KEY` is set correctly in `backend/.env`

```bash
curl http://localhost:5000/api/cards
```

### 3. Test with Frontend

If you also want to test the frontend locally:

1. In a new terminal, navigate to the `Frontend` directory:
```bash
cd Frontend
npm install
npm run dev
```

2. Update `Frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

3. Access frontend at: http://localhost:5173

## Environment Variables

### Backend Environment Variables

Create or update `backend/.env` with your configuration:

```env
# Flask Configuration
FLASK_ENV=production          # or "development"
FLASK_DEBUG=False             # or "True"

# Security (Change these in production!)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Clash Royale API
CLASH_ROYALE_API_KEY=your-api-key-from-developer.clashroyale.com

# Database (optional for local testing)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=cr

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174

# Caching
PLAYER_CACHE_DURATION=300
CARDS_CACHE_DURATION=86400

# Other Settings
ITEMS_PER_PAGE=20
JWT_ACCESS_TOKEN_HOURS=1
JWT_REFRESH_TOKEN_DAYS=30
```

## Common Issues & Troubleshooting

### Issue: Port 5000 Already in Use

**Solution:** Change the PORT environment variable:

#### Windows:
```batch
set PORT=5001
python deploy_local.bat
```

#### Linux/macOS:
```bash
PORT=5001 ./deploy_local.sh
```

#### Python:
```bash
PORT=5001 python deploy_local.py
```

### Issue: "ModuleNotFoundError: No module named 'gunicorn'"

**Solution:** Install gunicorn:
```bash
pip install gunicorn
```

The deployment scripts should auto-install it, but if not, run the above command.

### Issue: "Failed to import wsgi"

Make sure you're running the script from the **project root directory** (where `backend/` and `Frontend/` folders are).

```bash
# ✅ Correct
python deploy_local.py

# ❌ Wrong
cd backend && python ../deploy_local.py
```

### Issue: API Key Not Working

1. Go to [https://developer.clashroyale.com/](https://developer.clashroyale.com/)
2. Create a **new API key**
3. Leave "Allowed IP addresses" **BLANK** for local testing
4. Copy the new key to `backend/.env`:

```env
CLASH_ROYALE_API_KEY=your-new-key-here
```

### Issue: CORS Errors When Calling from Frontend

Ensure `CORS_ORIGINS` in `backend/.env` includes your frontend URL:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174
```

Then restart the backend.

### Issue: Database Errors

For local testing, the backend uses SQLite by default. If you see database errors:

1. Delete the old database:
   ```bash
   cd backend
   rm clash_royale_dev.db
   ```

2. Restart the backend - it will create a new database

## Comparing Modes

| Feature | Production (Gunicorn) | Development (Flask) |
|---------|----------------------|-------------------|
| **Workers** | 4 | 1 |
| **Hot-Reload** | ✅ (for testing) | ✅ |
| **Performance** | High | Lower |
| **Error Messages** | Minimal | Detailed |
| **Startup Time** | Instant | Instant |
| **Use Case** | Testing Render setup | Development |
| **Matches Render** | ✅ Yes | ❌ No |

## Next Steps

### After Local Testing

1. **Test Production Mode** - Run Mode 1 (Gunicorn) to verify it works like Render
2. **Commit Your Changes** - Push to GitHub:
   ```bash
   git add deploy_local.* backend/wsgi.py
   git commit -m "Add local Render deployment simulator"
   git push
   ```
3. **Deploy to Render** - Go to your Render dashboard and manually deploy or push a new commit

### Monitoring

Each deployment mode shows detailed logs:

**Production Mode Output:**
```
[2026-02-12 10:30:45 +0000] [1234] [INFO] Listening at: http://0.0.0.0:5000
[2026-02-12 10:30:45 +0000] [1234] [INFO] Using worker: sync
[2026-02-12 10:30:45 +0000] [1238] [INFO] Booting worker with pid: 1238
```

**Development Mode Output:**
```
WARNING in app.run_server (dev server thread)
WARNING in app.run_server (dev server thread)
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

## Additional Resources

- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Render Deployment Guide](RENDER_DEPLOYMENT.md)
- [Render Quick Start](RENDER_QUICK_START.md)

## Need Help?

If something doesn't work:

1. Check the logs in the terminal
2. Verify your API key is valid
3. Ensure port 5000 is not in use
4. Make sure you're in the project root directory
5. Check [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for more details
