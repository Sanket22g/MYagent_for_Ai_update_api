# Deployment Guide for Render

This guide explains how to deploy the AI Agent App API to Render.

## Key Differences from Netlify

Render uses traditional web services instead of serverless functions:
- ✅ Scheduler runs continuously (9 AM daily reports work!)
- ✅ FastAPI runs directly with Uvicorn (no Mangum adapter needed)
- ✅ Better for always-on services
- ✅ Free tier includes 750 hours/month (enough for continuous running)

## Prerequisites

1. **GitHub Repository** - Already set up at: `https://github.com/Sanket22g/MYagent_for_Ai_update_api.git`
2. **Render Account** - Sign up at [https://render.com](https://render.com)
3. **MongoDB Atlas URI** - Already configured (should be in your `.env`)
4. **API Keys** - SERPER_API_KEY, GEMINI_API_KEY, YOUTUBE_API_KEY

## Deployment Method 1: Docker (Recommended)

### Step 1: Create a New Web Service on Render

1. Log in to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect GitHub repository: Search for `MYagent_for_Ai_update_api`
4. Select the repository and **main** branch

### Step 2: Configure Service

**Service Settings:**
- **Name**: `ai-agent-api`
- **Environment**: `Docker`
- **Region**: Pick closest to you (e.g., `us-east-1`)
- **Plan**: `Free` (for testing) or `Standard` (for production)

**Build Settings:**
- **Docker file path**: `./Dockerfile`
- **Docker context**: `/`

### Step 3: Add Environment Variables

In the **Environment** section, add these variables:

```
MONGODB_URI=mongodb+srv://sanket800730_db_user:UtalsdZQ7IOpyZj2@cluster0.tpocqwo.mongodb.net/?appName=Cluster0
MODEL=gpt-4o-mini
SERPER_API_KEY=<your-serper-api-key>
GEMINI_API_KEY=<your-gemini-api-key>
YOUTUBE_API_KEY=<your-youtube-api-key>
DISABLE_SCHEDULER=false
```

⚠️ **Security**: These are secret keys—use Render's secret management or encrypt them.

### Step 4: Deploy

1. Click **Create Web Service**
2. Render will build and deploy automatically (takes 5-10 min)
3. Once deployed, check health: `https://<your-service-name>.onrender.com/health`

---

## Deployment Method 2: Native (Without Docker)

If you prefer not to use Docker:

### Step 1: Create a New Web Service

1. Log in to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect GitHub repository: `MYagent_for_Ai_update_api`

### Step 2: Configure Service

**Service Settings:**
- **Name**: `ai-agent-api`
- **Environment**: `Python 3`
- **Region**: Pick closest to you
- **Plan**: `Free`

**Build & Start Commands:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn ai_agent_app_for_summary.api:app --host 0.0.0.0 --port 8000`

### Step 3: Add Environment Variables

Same as Method 1 (see above).

### Step 4: Deploy

Click **Create Web Service** and wait for deployment.

---

## Testing Your Deployment

Once deployed, test these endpoints:

### 1. Health Check
```bash
curl https://<your-service-name>.onrender.com/health
```
Expected response:
```json
{
  "status": "ok",
  "uptime": 123.45,
  "report_status": "idle"
}
```

### 2. Get Latest Report
```bash
curl https://<your-service-name>.onrender.com/report
```

### 3. Generate New Report (Manual Trigger)
```bash
curl -X POST https://<your-service-name>.onrender.com/crew/start \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI LLMs, agentic ai, rag, and new ai technology", "source": "api"}'
```

### 4. Check Status
```bash
curl https://<your-service-name>.onrender.com/status
```

### 5. List Scheduler Jobs
```bash
curl https://<your-service-name>.onrender.com/scheduler/jobs
```

---

## Daily Scheduler

The scheduler runs **daily at 9:00 AM (UTC)** automatically:

1. Wakes up at 9 AM
2. Runs the crew to generate AI research summary
3. Saves report to MongoDB
4. Returns to sleep until next day

You can also trigger manually via API:
```bash
curl -X POST https://<your-service-name>.onrender.com/crew/start
```

---

## MongoDB Integration

Your reports are saved to MongoDB Atlas:

**Database:** `cluster0`
**Collection:** `ai_research_reports`

Each report contains:
- `_id`: Unique document ID
- `topic`: Research topic
- `topics`: Array of 7 topics with key takeaways and YouTube videos
- `summary`: Overall summary
- `created_at`: Timestamp
- `source`: "api" or "scheduler"

**Query recent reports:**
```javascript
db.ai_research_reports.find().sort({created_at: -1}).limit(5)
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/report` | GET | Get latest report from MongoDB |
| `/crew/start` | POST | Manually trigger report generation |
| `/status` | GET | Get current run status |
| `/scheduler/jobs` | GET | List scheduled jobs |

---

## Troubleshooting

### Build Fails with "AttributeError: module 'os' has no attribute 'sched_getaffinity'"

**Solution:** Python 3.14+ has removed this method. Render uses 3.13 by default—no fix needed.

### Scheduler Not Running

**Check:** Is `DISABLE_SCHEDULER` set to `false`?
```bash
# In Render dashboard → Environment tab
DISABLE_SCHEDULER=false
```

### MongoDB Connection Fails

1. Verify `MONGODB_URI` is correct
2. Check MongoDB Atlas IP whitelist is open to `0.0.0.0/0`
3. Test locally: `uv run python -c "from ai_agent_app_for_summary.mongo_store import get_latest_report; print(get_latest_report())"`

### API Returns 502 Bad Gateway

1. Check Render logs: Dashboard → Logs tab
2. Verify all environment variables are set
3. Test health endpoint: `https://<your-service-name>.onrender.com/health`

---

## Environment Variables Checklist

Before deploying, ensure these are configured:

- [ ] `MONGODB_URI` - MongoDB Atlas connection string
- [ ] `MODEL` - LLM model (e.g., `gpt-4o-mini`)
- [ ] `SERPER_API_KEY` - Serper API key for news search
- [ ] `GEMINI_API_KEY` - Google Gemini API key
- [ ] `YOUTUBE_API_KEY` - YouTube API key
- [ ] `DISABLE_SCHEDULER` - Set to `false` to enable 9 AM scheduler

---

## Monitoring & Logs

### View Logs

In Render dashboard → Your service → Logs tab

### Monitor CPU/Memory

In Render dashboard → Your service → Metrics tab

### Set Up Alerts

Render Pro allows email alerts for deployment failures.

---

## Cost Estimate

**Free Tier:**
- 750 hours/month included
- Auto-sleeps after 15 min of inactivity
- Perfect for testing

**Standard Plan (Production):**
- Continuous uptime
- $7/month
- Recommended for daily scheduler

---

## Next Steps

1. ✅ Verify code is pushed to GitHub main branch
2. ✅ Create Render account and connect GitHub
3. ✅ Deploy using Method 1 (Docker) or Method 2 (Native)
4. ✅ Test health endpoint
5. ✅ Configure your Android app to call the Render API URL
6. ✅ (Optional) Set up monitoring and alerts

---

## Android App Integration

Once deployed, provide your Android team with this base URL:
```
https://<your-service-name>.onrender.com
```

Example endpoint:
```
https://<your-service-name>.onrender.com/report
```

See [API Documentation](./API_ENDPOINTS.md) for full endpoint specs.
