# Quick Render Deployment Guide

## 5-Minute Setup

### 1. GitHub Setup
- Ensure your code is pushed to GitHub
- Your repository should have a public link

### 2. Create Backend Service
Visit [https://dashboard.render.com/](https://dashboard.render.com/) and:

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `tuxhuz-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn -w 1 -b 0.0.0.0:$PORT wsgi:app`
   - **Plan**: Free

4. Click **"Create Web Service"**
5. **Wait for deployment** (takes 2-3 minutes)
6. Copy your backend URL (e.g., `https://tuxhuz-backend.onrender.com`)

### 3. Set Backend Environment Variables

In your backend service → **Environment**, add:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-random-string>
JWT_SECRET_KEY=<generate-random-string>
CLASH_ROYALE_API_KEY=<your-api-key>
CORS_ORIGINS=https://tuxhuz-frontend.onrender.com
```

### 4. Create Frontend Service

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `tuxhuz-frontend`
   - **Root Directory**: `Frontend`
   - **Build**: `npm install && npm run build`
   - **Publish**: `dist`

4. Click **"Create Static Site"**

### 5. Set Frontend Environment Variables

In frontend service → **Environment Variable**, add:

```
VITE_API_BASE_URL=https://tuxhuz-backend.onrender.com/api
```

(Replace `tuxhuz-backend` with your actual backend service name)

## Done! ✅

Your app is now live:
- **Frontend**: https://tuxhuz-frontend.onrender.com
- **Backend**: https://tuxhuz-backend.onrender.com

### Auto-Deployment
Each time you push to GitHub, both services redeploy automatically.

## Troubleshooting

### Frontend shows 404 errors?
- Check `VITE_API_BASE_URL` matches your backend URL
- Rebuild frontend manually in Render dashboard

### Backend won't start?
- Check logs in Render dashboard
- Verify all environment variables are set
- Ensure `requirements.txt` is in `backend/` folder

### CORS errors?
- Update `CORS_ORIGINS` environment variable to match your frontend URL

## Get Your API Key
1. Go to [developer.clashroyale.com](https://developer.clashroyale.com/)
2. Sign in with Supercell ID
3. Create API key
4. Set `CLASH_ROYALE_API_KEY` environment variable

## Need More Help?
See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.
