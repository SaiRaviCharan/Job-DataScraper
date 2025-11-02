# Deploy Jobscraper - Step by Step (FREE!)

**Total Time**: 15 minutes | **Cost**: $0 | **No credit card needed**

---

## ✅ Prerequisites

- ✅ Code pushed to GitHub (done!)
- ✅ GitHub account (have it)
- ✅ Free accounts on Render + Vercel (we'll create)

---

## 🚀 Step 1: Deploy Backend to Render (5 min)

### 1a. Sign Up

1. Go to https://render.com
2. Click "Sign up" → "Continue with GitHub"
3. Authorize Render
4. Choose free plan

### 1b. Create Web Service

1. Click "New +" (top right)
2. Select "Web Service"
3. Select your `Job-DataScraper` repo
4. Fill in details:
   - **Name**: `jobdatascraper`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.app:app`
   - **Region**: Choose closest region
5. Click "Create Web Service"

### 1c. Add Environment Variables

While deploying, go to **Environment** tab:

```
GEMINI_API_KEY = your_actual_api_key_here
FLASK_DEBUG = 0
```

Click **Add Variable** for each one.

### 1d. Wait for Deployment

- Takes 3-5 minutes
- Watch the logs
- Should end with: `Listening on 0.0.0.0:10000`

### 1e. Get Your Backend URL

- Dashboard shows: `https://jobdatascraper.onrender.com`
- **Save this URL!** (needed for frontend)

### ✅ Test Backend

```
Visit: https://jobdatascraper.onrender.com/health
Should show: {"status": "ok"}
```

---

## 🎨 Step 2: Deploy Frontend to Vercel (5 min)

### 2a. Sign Up

1. Go to https://vercel.com
2. Click "Sign up" → "Continue with GitHub"
3. Authorize Vercel
4. Skip team creation

### 2b. Import Project

1. Click "Add New..." (top left)
2. Select "Project"
3. Select your `Job-DataScraper` repo
4. Vercel auto-detects settings, BUT:
   - **Root Directory**: Change to `./frontend`
   - **Framework**: Should be "React"
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 2c. Add Environment Variables

Before deploying, add:

```
REACT_APP_API_BASE = https://jobdatascraper.onrender.com
```

(Use your actual Render backend URL from Step 1)

### 2d. Deploy

Click "Deploy"

- Takes 2-3 minutes
- Watch progress bar

### 2e. Get Your Frontend URL

- Vercel shows: `https://jobdatascraper.vercel.app`
- This is your public app URL!

---

## ✅ Step 3: Verify Everything Works (2 min)

### 3a. Test Frontend

1. Visit: https://jobdatascraper.vercel.app
2. Search for: `python`
3. Click: **⚡ Scrape Jobs**
4. Should show: Jobs list, skills, salaries

### 3b. Test API

From browser console or terminal:

```bash
curl https://jobdatascraper.onrender.com/health
# Should return: {"status": "ok"}
```

### 3c. Check Logs

**Render Logs**:
- Go to Render dashboard
- Select `jobdatascraper` service
- View "Logs" tab
- Should see requests from frontend

---

## 🔄 Auto-Deploy (Already Enabled!)

Both Render and Vercel auto-deploy:

```
1. Make changes locally
2. Push to GitHub main branch
3. Render/Vercel see the change
4. Auto-redeploy (3-5 minutes)
```

No manual deploys needed! 🎉

---

## 🛠️ Keeping Backend Awake (Free Tier Trick)

Render free tier spins down after 15 min of inactivity.

### Option A: Use UptimeRobot (Recommended)

1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add Monitor:
   - **URL**: `https://jobdatascraper.onrender.com/health`
   - **Check Interval**: 5 minutes
4. Pings every 5 min = always awake!

### Option B: Manual Workaround

Visit your app regularly (keeps it awake).

---

## 🔒 Environment Variables Reference

### Render Backend
```
GEMINI_API_KEY = your_key_here
FLASK_DEBUG = 0
```

### Vercel Frontend
```
REACT_APP_API_BASE = https://jobdatascraper.onrender.com
```

---

## 🚨 Troubleshooting

### "Service Suspended" on Render
- Free tier auto-spins down after 15 min
- **Fix**: Use UptimeRobot (above)
- Or: Visit the app every 10 minutes

### "API Error" on Frontend
- Check Vercel env var: `REACT_APP_API_BASE`
- **Fix**: Go to Vercel → Settings → Environment
- Make sure URL matches your Render backend

### "Module Not Found"
- Problem: Missing Python dependencies
- **Fix**: Add to `requirements.txt`, push to GitHub
- Render auto-redeploys

### "CORS Error"
- Backend has CORS enabled
- **Fix**: Clear browser cache, try incognito
- Check both URLs are live

---

## 📊 Live URLs (After Deployment)

```
Frontend: https://jobdatascraper.vercel.app
Backend:  https://jobdatascraper.onrender.com
API Test: https://jobdatascraper.onrender.com/health
```

---

## 💰 Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| Render Backend | Free | $0 |
| Vercel Frontend | Free | $0 |
| UptimeRobot | Free | $0 |
| **Total** | | **$0/month** 🎉 |

---

## ✨ What's Live Now

✅ Full-stack job scraper app  
✅ Real-time job search  
✅ AI-powered summaries  
✅ Skills analysis  
✅ Salary data  
✅ Auto-deploy from GitHub  
✅ 100% free hosting  

---

## 📝 Next Steps

1. ✅ Deploy backend (Render) - **Done!**
2. ✅ Deploy frontend (Vercel) - **Done!**
3. ✅ Set UptimeRobot monitor - **Optional**
4. ✅ Share your app!
   - Vercel URL to portfolio
   - GitHub repo link
   - LinkedIn post?

---

## 🎉 You're Done!

Your job scraper is now **LIVE** and **FREE**!

Visit: https://jobdatascraper.vercel.app

**Enjoy! 🚀**
