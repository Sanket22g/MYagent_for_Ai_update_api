# Quick Start: Deploy to Render in 5 Minutes

## Step 1: Prepare Your Code (Local)

```bash
# Ensure all changes are committed
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

## Step 2: Create Render Service

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Select repository: `MYagent_for_Ai_update_api`
4. Branch: `main`

## Step 3: Configure Service

**For Docker deployment (recommended):**
- Environment: Docker
- Build file: `./Dockerfile`

**For Native Python:**
- Environment: Python 3
- Build: `pip install -r requirements.txt`
- Start: `uvicorn ai_agent_app_for_summary.api:app --host 0.0.0.0 --port 8000`

## Step 4: Add Environment Variables

Copy these into Render environment tab:

```
MONGODB_URI=mongodb+srv://sanket800730_db_user:UtalsdZQ7IOpyZj2@cluster0.tpocqwo.mongodb.net/?appName=Cluster0
MODEL=gpt-4o-mini
SERPER_API_KEY=<your-key>
GEMINI_API_KEY=<your-key>
YOUTUBE_API_KEY=<your-key>
DISABLE_SCHEDULER=false
```

## Step 5: Deploy

Click **Create Web Service** → Wait 5-10 min → Done! ✅

## Step 6: Test

```bash
# Replace <service-name> with your actual Render service name
curl https://<service-name>.onrender.com/health
```

## Your API is NOW LIVE at:
```
https://<service-name>.onrender.com
```

## Share with Android Team:
```
Base URL: https://<service-name>.onrender.com
Report endpoint: GET /report
Generate report: POST /crew/start
```

---

## Files Created for Render:

| File | Purpose |
|------|---------|
| `render.yaml` | Infrastructure as Code configuration |
| `Dockerfile` | Container build instructions |
| `.dockerignore` | Exclude files from Docker build |
| `RENDER_DEPLOYMENT.md` | Full deployment documentation |

## Scheduler Benefit on Render

Unlike Netlify Functions, Render keeps your app running 24/7, so:
- ✅ Daily 9 AM reports generate automatically
- ✅ No manual triggers needed
- ✅ MongoDB stores all historical reports
- ✅ Android app always has latest data available

## Need Help?

See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) for:
- Troubleshooting
- Monitoring logs
- Cost information
- MongoDB integration details
