# API Quick Reference for Android Devs

## 🔗 Base URL
```
https://<your-service-name>.onrender.com
```

## 📡 5 Main Endpoints

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| `GET` | `/health` | Check if API is alive | `{"status": "ok"}` |
| `GET` | `/report` | Get latest AI research report | Full report JSON |
| `POST` | `/crew/start` | Start new report generation | `{"status": "queued"}` |
| `GET` | `/status` | Check generation progress | `{"status": "running", "progress": 60}` |
| `GET` | `/scheduler/jobs` | View daily schedule | `{"jobs": [...], "next_run": "..."}` |

---

## ⚡ Quick Start: Generate & Display Report

### Step 1: Verify API is Running
```bash
curl https://<your-service-name>.onrender.com/health
```
Success = `{"status": "ok"}`

### Step 2: Start Report Generation
```bash
curl -X POST https://<your-service-name>.onrender.com/crew/start \
  -H "Content-Type: application/json" \
  -d '{"source": "api"}'
```
Response:
```json
{"status": "queued", "estimated_time_seconds": 180}
```

### Step 3: Poll for Completion (every 5 sec)
```bash
curl https://<your-service-name>.onrender.com/status
```
Responses:
- `"status": "queued"` → Still waiting
- `"status": "running"`, `"progress_percent": 45` → In progress
- `"status": "completed"` → Ready!

### Step 4: Get Report
```bash
curl https://<your-service-name>.onrender.com/report
```

---

## 📱 Android Implementation Template

```kotlin
// 1. Define data classes
data class Report(
    val _id: String,
    val topic: String,
    val summary: String,
    val topics: List<Topic>,
    val created_at: String,
    val source: String
)

data class Topic(
    val title: String,
    val key_takeaways: List<String>,
    val youtube_videos: List<Video>,
    val related_links: List<Link>
)

data class Video(
    val title: String,
    val url: String,
    val channel: String,
    val duration_minutes: Int
)

data class Link(
    val title: String,
    val url: String
)

// 2. Create API interface
interface AIAgentAPI {
    @GET("/report")
    suspend fun getReport(): Report?
    
    @POST("/crew/start")
    suspend fun startGeneration(): GenerateResponse
    
    @GET("/status")
    suspend fun getStatus(): StatusResponse
}

// 3. Generate & Display
lifecycleScope.launch {
    try {
        // Start generation
        api.startGeneration()
        
        // Poll until done
        var isDone = false
        repeat(120) { // Max 10 minutes
            val status = api.getStatus()
            if (status.status == "completed") {
                isDone = true
                return@repeat
            }
            delay(5000) // Wait 5 seconds
        }
        
        // Get report
        if (isDone) {
            val report = api.getReport()
            // Display using report.topics, report.summary, etc.
        }
    } catch (e: Exception) {
        showError(e.message)
    }
}
```

---

## 📊 Report Structure (What You Get)

```
Report {
  summary: "Main overview..."
  topics: [
    {
      title: "Topic 1"
      key_takeaways: ["point 1", "point 2", "point 3"]
      youtube_videos: [
        {
          title: "...",
          url: "https://youtube.com/...",
          channel: "...",
          duration_minutes: 15
        },
        {...} // 2nd video
      ]
      related_links: [
        {
          title: "...",
          url: "https://..."
        }
      ]
    },
    {...} // Topics 2-7
  ]
}
```

---

## ✅ Response Examples

### Success: Getting Report
```json
{
  "_id": "67f8c3a4...",
  "topic": "AI LLMs, agentic ai, rag, and new ai technology",
  "summary": "This week marked breakthrough moments...",
  "topics": [
    {
      "title": "Large Language Models",
      "key_takeaways": [
        "GPT-5 now supports 1M context window",
        "Open-source LLMs catching up",
        "Multi-modal capabilities standard"
      ],
      "youtube_videos": [
        {
          "title": "GPT-5 Explained",
          "url": "https://youtube.com/watch?v=...",
          "channel": "TechCrunch",
          "duration_minutes": 15
        }
      ],
      "related_links": [
        {
          "title": "OpenAI Blog",
          "url": "https://openai.com/blog/..."
        }
      ]
    }
    // ... 6 more topics
  ],
  "created_at": "2026-03-28T09:00:15Z"
}
```

### Success: Generation Started
```json
{
  "status": "queued",
  "estimated_time_seconds": 180
}
```

### In Progress
```json
{
  "status": "running",
  "progress_percent": 60,
  "current_phase": "youtube_research"
}
```

### Completed
```json
{
  "status": "completed",
  "total_seconds": 342
}
```

---

## 🚨 Error Handling

| Code | Meaning | Handle |
|------|---------|--------|
| 200 | Success | Use response |
| 202 | Accepted | Continue polling |
| 204 | No Content | No report yet, generate one |
| 429 | Rate Limited | Wait 60 sec, retry |
| 500 | Server Error | Retry after 30 sec |
| 503 | Unavailable | Retry after 1 min |

---

## 🕐 Automatic Daily Reports

The API generates reports **automatically every day at 9:00 AM (UTC)**

Just call `GET /report` in your app to display the latest! 

Check next run time:
```bash
curl https://<your-service-name>.onrender.com/scheduler/jobs
# Response includes "next_run": "2026-03-29T09:00:00Z"
```

---

## 💡 Best Practices

✅ **DO:**
- Cache report locally on first load
- Show last updated time to user
- Allow manual refresh button
- Handle errors gracefully
- Show loading spinner during poll
- Respect 5-sec poll interval

❌ **DON'T:**
- Poll `/status` more than every 5 seconds
- Make calls to `/crew/start` rapidly
- Ignore HTTP error codes
- Display error codes to user (show friendly messages)
- Poll forever (max 10 minutes)

---

## 🔗 Share with Your Team

Base URL: `https://<your-service-name>.onrender.com`

**Available 24/7**
Daily reports at 9 AM UTC
Reports stored indefinitely

For full API docs: See `API_DOCUMENTATION.md`
