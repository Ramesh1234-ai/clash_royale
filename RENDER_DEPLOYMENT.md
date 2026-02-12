# Deploying TuxHuz on Render

This guide walks you through deploying both the backend and frontend of TuxHuz to Render.

## Prerequisites

1. A [Render account](https://render.com)
2. Your code pushed to a GitHub repository
3. A Clash Royale API key from [developer.clashroyale.com](https://developer.clashroyale.com/)

## Architecture Overview

- **Backend**: Flask API (Python) → Render Web Service
- **Frontend**: React + Vite → Render Static Site
- **Database**: PostgreSQL (recommended for Render) or MySQL

## Step 1: Prepare Your Repository

### 1.1 Update Backend Dockerfile for Production

Modify [backend/Dockerfile](backend/Dockerfile) to remove the `--reload` flag for production:

```dockerfile
# Remove --reload from the CMD line
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 1.2 Create render.yaml

Create a `render.yaml` file in the root directory of your repository:

```yaml
services:
  - type: web
    name: tuxhuz-backend
    env: python
    plan: free
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && gunicorn -w 1 -b 0.0.0.0:$PORT wsgi:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_DEBUG
        value: "False"
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: CLASH_ROYALE_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: tuxhuz-db
          property: connectionString
      - key: CORS_ORIGINS
        value: "https://tuxhuz-frontend.onrender.com"
      - key: PORT
        value: "5000"

  - type: static
    name: tuxhuz-frontend
    buildCommand: cd Frontend && npm install && npm run build
    staticPublishPath: Frontend/dist
    envVars:
      - key: VITE_API_BASE_URL
        value: "https://tuxhuz-backend.onrender.com/api"

  - type: pserv
    name: tuxhuz-db
    ipAllowList: []
    plan: free
    dbName: tuxhuz_db
    dbUser: tuxhuz_user
    postgresMajorVersion: 15
```

> **Note**: Replace service names if they conflict with existing services.

## Step 2: Deploy via Render Dashboard (Recommended)

### Option A: Using Github Integration (Easiest)

1. Go to [https://dashboard.render.com/](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Select **"Build and deploy from a Git repository"**
4. Connect your GitHub account and select your TuxHuz repository
5. Configure the service:
   - **Name**: `tuxhuz-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - **Plan**: Free tier (or paid for production)

6. Click **"Create Web Service"**
7. Go to **Environment** tab and add these variables:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-a-random-string>
JWT_SECRET_KEY=<generate-another-random-string>
CLASH_ROYALE_API_KEY=<your-api-key>
MYSQL_HOST=<your-mysql-host>
MYSQL_USER=<your-mysql-user>
MYSQL_PASSWORD=<your-mysql-password>
MYSQL_DATABASE=clash_royale_db
CORS_ORIGINS=https://tuxhuz-frontend.onrender.com
```

### Creating the Frontend Service

1. Click **"New +"** → **"Static Site"**
2. Configure:
   - **Name**: `tuxhuz-frontend`
   - **Root Directory**: `Frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

3. Add Environment Variables:
```env
VITE_API_BASE_URL=https://tuxhuz-backend.onrender.com/api
```

4. Click **"Create Static Site"**

## Step 3: Configure Environment Variables

### Backend Environment Variables

In your Render backend service dashboard, set:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# Security (generate strong random strings)
SECRET_KEY=your-random-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Clash Royale API
CLASH_ROYALE_API_KEY=your-actual-api-key-from-developer.clashroyale.com

# Database (if using MySQL)
MYSQL_HOST=your-mysql-host
MYSQL_PORT=3306
MYSQL_USER=your-db-user
MYSQL_PASSWORD=your-db-password
MYSQL_DATABASE=clash_royale_db

# Or use PostgreSQL (recommended on Render)
DATABASE_URL=postgresql://user:password@host:port/dbname

# CORS - Update with your frontend URL
CORS_ORIGINS=https://tuxhuz-frontend.onrender.com

# Caching
PLAYER_CACHE_DURATION=300
CARDS_CACHE_DURATION=86400
```

### Frontend Environment Variables

In your Render frontend service dashboard, set:

```env
VITE_API_BASE_URL=https://tuxhuz-backend.onrender.com/api
```

## Step 4: Update Backend for PostgreSQL (Optional but Recommended)

Render provides free PostgreSQL databases. Update your `requirements.txt`:

```diff
+ psycopg2-binary==2.9.9
```

Then modify [backend/config.py](backend/config.py):

```python
# PostgreSQL Database configuration (for Render)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
elif ENVIRONMENT == 'development':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clash_royale_dev.db'
else:
    # MySQL fallback
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        "?charset=utf8mb4"
    )
```

## Step 5: Deploy Database

### Using PostgreSQL on Render:

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `tuxhuz-db`
   - **Database**: `tuxhuz_db`
   - **User**: `tuxhuz_user`
3. Create the database
4. Copy the `DATABASE_URL` connection string
5. Add it as an environment variable in your backend service: `DATABASE_URL=<your-connection-string>`

### Initialize Database

The database will initialize when the Flask app first runs (using `init_db.py`).

## Step 6: Connect Frontend to Backend

Update [Frontend/.env](Frontend/.env):

```env
VITE_API_BASE_URL=https://tuxhuz-backend.onrender.com/api
```

> Replace `tuxhuz-backend` with your actual backend service name on Render.

## Step 7: Deploy

### Option 1: Auto-Deploy from GitHub (Recommended)

Once configured, every push to your GitHub repo will automatically trigger a new deployment.

### Option 2: Manual Deploy

1. Go to your service dashboard on Render
2. Click **"Manual Deploy"** → **"Deploy Latest Commit"**

## Monitoring and Logs

- **Backend Logs**: Dashboard → Service → Logs tab
- **Frontend Logs**: Dashboard → Static Site → Logs tab
- **Database**: Dashboard → PostgreSQL → instance page

## Troubleshooting

### Backend Not Starting?

1. Check logs: Dashboard → Logs
2. Verify environment variables are set
3. Ensure `requirements.txt` is in the correct directory

```bash
# Test locally first
pip install -r backend/requirements.txt
python -m flask run
```

### Frontend Not Loading API?

1. Check `VITE_API_BASE_URL` is correct in Frontend environment variables
2. Verify `CORS_ORIGINS` on backend includes frontend URL
3. Check browser console for CORS errors

### Database Connection Issues?

1. Verify `DATABASE_URL` or MySQL credentials
2. Check network connectivity in Render dashboard
3. Run `python init_db.py` in backend service

## FAQ

**Q: How do I update my code after deploying?**
A: Just push to GitHub. Render will automatically redeploy.

**Q: Can I use the free tier?**
A: Yes, but services will spin down after 15 minutes of inactivity (Plan A). Use paid plans for production.

**Q: How do I add custom domain?**
A: Render Dashboard → Settings → Custom Domain

**Q: How do I enable HTTPS?**
A: Render provides free SSL/TLS certificates automatically.

## Production Checklist

- [ ] Environment variables set securely
- [ ] Database configured and initialized
- [ ] CORS origins updated to your domain
- [ ] API key valid
- [ ] Frontend `.env` updated with correct API URL
- [ ] Backend not in DEBUG mode
- [ ] Testing both services work together
- [ ] Monitoring/logging configured

## Support

- [Render Documentation](https://render.com/docs)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode)
