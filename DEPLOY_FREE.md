# 🚀 Deploy Jobscraper - FREE Hosting Platforms

**No credit card required! 100% free tier available.**

---

## Option 1: Render (Recommended for Backend) ⭐

**Free tier includes:**
- ✅ 750 hours/month free compute
- ✅ PostgreSQL database (free)
- ✅ Automatic deployments from GitHub
- ✅ Custom domain support

### Deploy Backend to Render

1. **Sign up**: https://render.com (connect GitHub)
2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Select your GitHub repo (Job-DataScraper)
   - Fill in:
     - **Name**: `jobdatascraper`
     - **Runtime**: `Python 3.11`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn backend.app:app`
   - Region: Choose closest to you

3. **Set Environment Variables**:
   - Click "Environment"
   - Add: `GEMINI_API_KEY=your_key_here`
   - Add: `FLASK_DEBUG=0`

4. **Deploy**:
   - Click "Deploy"
   - Wait 3-5 minutes
   - Get your URL: `https://jobdatascraper.onrender.com`

**Test**: `https://jobdatascraper.onrender.com/health`

---

## Option 2: Railway.app (Backend Alternative)

**Free tier includes:**
- ✅ $5 free credit/month
- ✅ GitHub auto-deploy
- ✅ Easy environment variables

### Deploy to Railway

1. **Sign up**: https://railway.app (GitHub login)
2. **New Project** → "Deploy from GitHub"
3. Select `Job-DataScraper` repo
4. Railway auto-detects Python
5. Add env vars:
   - `GEMINI_API_KEY=your_key`
   - `FLASK_DEBUG=0`
6. Get URL from "Deployments" tab

---

## Option 3: Vercel (Frontend) ⭐

**Free tier includes:**
- ✅ Unlimited deployments
- ✅ Custom domains
- ✅ GitHub auto-deploy
- ✅ Environment variables

### Deploy Frontend to Vercel

1. **Sign up**: https://vercel.com (GitHub login)
2. **Import Project**:
   - Select your `Job-DataScraper` repo
   - Framework: React
   - Root Directory: `./frontend`

3. **Environment Variables**:
   - `REACT_APP_API_BASE=https://jobdatascraper.onrender.com`
   - (use your Render/Railway backend URL)

4. **Deploy**:
   - Click "Deploy"
   - Wait for build
   - Get URL: `https://jobdatascraper.vercel.app`

---

## Option 4: Netlify (Frontend Alternative)

**Free tier includes:**
- ✅ Unlimited sites
- ✅ GitHub auto-deploy
- ✅ Edge functions
- ✅ Analytics

### Deploy to Netlify

1. **Sign up**: https://netlify.com (GitHub login)
2. **New Site** → "Import from Git"
3. Select your repo
4. **Build Settings**:
   - Base Directory: `frontend`
   - Build Command: `npm run build`
   - Publish Directory: `build`

5. **Environment Variables**:
   - `REACT_APP_API_BASE=https://jobdatascraper.onrender.com`

6. **Deploy**: Automatic on push to main

---

## Option 5: PythonAnywhere (Backend)

**Free tier includes:**
- ✅ 100MB disk space
- ✅ Web app hosting
- ✅ Easy Python setup

### Deploy to PythonAnywhere

1. **Sign up**: https://pythonanywhere.com (free account)
2. **Upload files**:
   - Use "Upload a file" or use git
   - Push your repo to your account

3. **Web app setup**:
   - Go to "Web" tab
   - Add new web app
   - Python 3.11 + Flask
   - Configure WSGI file

4. **Set environment variables**:
   - In web app settings, add:
   - `GEMINI_API_KEY=your_key`

5. **Reload** and get URL

---

## 📊 Recommended Setup

### **BEST: Render + Vercel** (100% Free)

```
┌─────────────────────────────────┐
│     GitHub (Your Repo)          │
│  Job-DataScraper (main branch)  │
└──────┬──────────────────┬───────┘
       │                  │
       ▼                  ▼
   ┌─────────┐        ┌─────────┐
   │ Render  │        │ Vercel  │
   │(Backend)│        │(Frontend)
   │ FREE    │        │ FREE    │
   └────┬────┘        └────┬────┘
        │                  │
        ▼                  ▼
https://jobdatascraper   https://jobdatascraper
  .onrender.com          .vercel.app
```

---

## Step-by-Step: Render + Vercel Deployment

### Step 1: Deploy Backend (Render)

```bash
# 1. Go to https://render.com
# 2. Sign in with GitHub
# 3. Click "New +" → "Web Service"
# 4. Select Job-DataScraper repo
# 5. Fill in:
#    - Name: jobdatascraper
#    - Runtime: Python 3.11
#    - Build Command: pip install -r requirements.txt
#    - Start Command: gunicorn backend.app:app
# 6. Click "Create Web Service"
# 7. Go to "Environment" → Add env vars:
#    - GEMINI_API_KEY=your_key
#    - FLASK_DEBUG=0
# 8. Wait 3-5 min, get URL from dashboard
```

**Backend URL**: `https://jobdatascraper.onrender.com`

### Step 2: Deploy Frontend (Vercel)

```bash
# 1. Go to https://vercel.com
# 2. Sign in with GitHub
# 3. Click "Add New..." → "Project"
# 4. Select Job-DataScraper repo
# 5. Build settings:
#    - Framework: React
#    - Root Directory: ./frontend
# 6. Add Environment Variable:
#    - Name: REACT_APP_API_BASE
#    - Value: https://jobdatascraper.onrender.com
# 7. Click "Deploy"
# 8. Get URL from dashboard
```

**Frontend URL**: `https://jobdatascraper.vercel.app`

---

## 🔗 Live URLs (After Deployment)

- **Frontend**: https://jobdatascraper.vercel.app
- **Backend API**: https://jobdatascraper.onrender.com
- **API Health**: https://jobdatascraper.onrender.com/health

---

## 🛠️ Keeping Apps Running (Free Tier)

### Render Free Tier Limitation
- Auto-spins down after 15 minutes of inactivity
- Spins back up on first request (~30s)
- **Solution**: Use free uptime bot

### Uptime Bot (Free)

Use **UptimeRobot** (free tier):

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add new monitor:
   - URL: `https://jobdatascraper.onrender.com/health`
   - Check interval: 5 minutes
4. Saves your backend from sleeping!

---

## 📝 Environment Variables

### Render Backend
```
GEMINI_API_KEY = your_actual_key_here
FLASK_DEBUG = 0
```

### Vercel Frontend
```
REACT_APP_API_BASE = https://jobdatascraper.onrender.com
```

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub main branch
- [ ] Render account created
- [ ] Backend deployed to Render
- [ ] Backend URL working (`/health` endpoint)
- [ ] Vercel account created
- [ ] Frontend deployed to Vercel
- [ ] Frontend can call backend API
- [ ] UptimeRobot monitor set (optional)
- [ ] Test live app

---

## 🧪 Test Your Deployment

### Test Backend
```bash
curl https://jobdatascraper.onrender.com/health
```

### Test Frontend
Visit: https://jobdatascraper.vercel.app
- Search for "python"
- Click "Scrape Jobs"
- Should see results!

---

## 🔄 Auto-Deploy Setup

Both Render and Vercel auto-deploy from GitHub!

```
1. Push changes to main branch
2. GitHub webhook triggers deployment
3. New version live in 2-5 minutes
```

No manual deploys needed! 🎉

---

## 💾 Free Tier Limits Summary

| Service | Free Tier | Limit |
|---------|-----------|-------|
| **Render** | Python Web | 750 hrs/mo |
| **Vercel** | Frontend | Unlimited |
| **Railway** | Compute | $5/mo credit |
| **PythonAnywhere** | Python | 100MB disk |
| **Netlify** | Frontend | Unlimited |

---

## 🆘 Troubleshooting

### "Service Suspended" on Render
- Free tier auto-spins down after 15 min
- Use UptimeRobot to keep alive
- Or upgrade to paid ($7/mo)

### "API Error" on Frontend
- Check `REACT_APP_API_BASE` env var on Vercel
- Rebuild: Go to "Deployments" → Redeploy
- Check backend is running: curl `/health`

### "Module not found" on Render
- Ensure `requirements.txt` has all deps
- Push changes to GitHub
- Render auto-redeploys

### "CORS Error"
- Backend already has CORS enabled
- Try clearing browser cache
- Check frontend/backend URLs match

---

## 💡 Cost Breakdown

- **Render Backend**: FREE (750 hrs/mo = ~31 days)
- **Vercel Frontend**: FREE (unlimited)
- **Domain**: FREE (.vercel.app, .onrender.com)
- **Uptime Bot**: FREE (UptimeRobot)
- **Total Cost**: **$0/month** 🎉

---

## 🚀 Next Steps

1. **Deploy Backend** (5 min)
   - Go to Render.com
   - Follow Step 1 above

2. **Deploy Frontend** (5 min)
   - Go to Vercel.com
   - Follow Step 2 above

3. **Test** (2 min)
   - Visit frontend URL
   - Search for jobs
   - Verify API calls work

4. **Share** (ongoing)
   - Frontend URL to portfolio
   - GitHub repo link
   - Live demo ready!

---

## 📞 Support Links

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **UptimeRobot**: https://uptimerobot.com
- **Your Repo**: https://github.com/SaiRaviCharan/Job-DataScraper

---

**All done! Your app is ready for FREE hosting.** 🎉
