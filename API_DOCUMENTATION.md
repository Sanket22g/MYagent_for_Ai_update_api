# AI Agent App API - Complete Documentation

**Live API URL:** `https://<your-service-name>.onrender.com`

---

## 📋 Table of Contents
1. [Base Information](#base-information)
2. [Endpoints](#endpoints)
3. [Response Schemas](#response-schemas)
4. [Examples](#examples)
5. [Error Handling](#error-handling)
6. [Status Codes](#status-codes)

---

## Base Information

### Authentication
- ✅ No authentication required
- All endpoints are public

### Base URL
```
https://<your-service-name>.onrender.com
```

### Response Format
- All responses are **JSON**
- Timestamps in **ISO 8601** format: `2026-03-28T14:30:45.123Z`

### Data Persistence
- Reports saved to **MongoDB**
- Accessible across all requests
- Historical data stored indefinitely
- **MongoDB connection** now includes improved SSL/TLS handling with certificate validation bypass and extended timeouts
- **Fallback to file storage** if MongoDB is temporarily unavailable

---

## Endpoints

### 1️⃣ GET `/health`
**Purpose:** Check if API is running and healthy

**Request:**
```bash
curl https://<your-service-name>.onrender.com/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "uptime": 1234.56,
  "report_status": "idle",
  "scheduler_active": true,
  "mongodb_connected": true
}
```

**Response Keys:**
- `status` (string): "ok" = healthy
- `uptime` (float): Seconds since API started
- `report_status` (string): "idle", "queued", "running", "completed", "failed"
- `scheduler_active` (boolean): Is 9 AM daily scheduler enabled?
- `mongodb_connected` (boolean): Is MongoDB reachable?

**Use Case:** App startup - verify API is alive before showing content

---

### 2️⃣ GET `/report`
**Purpose:** Get the latest AI research report

**Request:**
```bash
curl https://<your-service-name>.onrender.com/report
```

**Response (200 OK):**
```json
{
  "_id": "67f8c3a4b1e9d2f3c5g7h9k0",
  "topic": "AI LLMs, agentic ai, rag, and new ai technology",
  "summary": "This week marked breakthrough moments in AI development...",
  "topics": [
    {
      "title": "Large Language Models",
      "key_takeaways": [
        "GPT-5 now supports 1M context window",
        "Open-source LLMs catching up to commercial models",
        "Multi-modal capabilities becoming standard"
      ],
      "youtube_videos": [
        {
          "title": "GPT-5 Explained",
          "url": "https://youtube.com/watch?v=...",
          "channel": "TechCrunch",
          "duration_minutes": 15
        },
        {
          "title": "LLM Training Secrets",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Yannic Kilcher",
          "duration_minutes": 45
        }
      ],
      "related_links": [
        {
          "title": "OpenAI Blog Post",
          "url": "https://openai.com/blog/gpt-5..."
        }
      ]
    },
    {
      "title": "Agentic AI",
      "key_takeaways": [
        "Autonomous agents solving complex workflows",
        "Multi-agent collaboration improving results",
        "Real-world deployment success stories"
      ],
      "youtube_videos": [
        {
          "title": "Building AI Agents",
          "url": "https://youtube.com/watch?v=...",
          "channel": "DeepLearning.AI",
          "duration_minutes": 30
        },
        {
          "title": "Agent Benchmarks",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Meta AI",
          "duration_minutes": 20
        }
      ],
      "related_links": [
        {
          "title": "Agent Research Paper",
          "url": "https://arxiv.org/..."
        }
      ]
    },
    {
      "title": "Retrieval Augmented Generation (RAG)",
      "key_takeaways": [
        "RAG improving accuracy by 40%",
        "Vector databases becoming essential",
        "Hybrid search combining BM25 + semantic"
      ],
      "youtube_videos": [
        {
          "title": "RAG Fundamentals",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Andrew Ng",
          "duration_minutes": 25
        },
        {
          "title": "Vector DB Showdown",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Weights & Biases",
          "duration_minutes": 35
        }
      ],
      "related_links": [
        {
          "title": "RAG Best Practices",
          "url": "https://pinecone.io/learn/..."
        }
      ]
    },
    {
      "title": "AI Ethics & Safety",
      "key_takeaways": [
        "New regulations in EU and US",
        "Alignment research advancing",
        "Transparency requirements increasing"
      ],
      "youtube_videos": [
        {
          "title": "AI Safety Explained",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Paul Christiano",
          "duration_minutes": 40
        },
        {
          "title": "AI Regulation Impact",
          "url": "https://youtube.com/watch?v=...",
          "channel": "SyntacticAI",
          "duration_minutes": 18
        }
      ],
      "related_links": [
        {
          "title": "UK AI Bill Analysis",
          "url": "https://www.gov.uk/..."
        }
      ]
    },
    {
      "title": "Computer Vision Advances",
      "key_takeaways": [
        "Vision transformers outperforming CNNs",
        "Real-time object detection on edge",
        "3D scene understanding improving"
      ],
      "youtube_videos": [
        {
          "title": "Vision Transformers Deep Dive",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Jeremy Howard",
          "duration_minutes": 50
        },
        {
          "title": "Edge Vision Models",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Qualcomm",
          "duration_minutes": 22
        }
      ],
      "related_links": [
        {
          "title": "Vision Paper Collection",
          "url": "https://paperswithcode.com/..."
        }
      ]
    },
    {
      "title": "Multimodal AI",
      "key_takeaways": [
        "Voice + text + image integration seamless",
        "Cross-modal reasoning breakthrough",
        "Production-ready multimodal APIs"
      ],
      "youtube_videos": [
        {
          "title": "Multimodal Foundations",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Stanford HAI",
          "duration_minutes": 38
        },
        {
          "title": "Voice AI Evolution",
          "url": "https://youtube.com/watch?v=...",
          "channel": "OpenAI",
          "duration_minutes": 12
        }
      ],
      "related_links": [
        {
          "title": "Multimodal Model Comparison",
          "url": "https://huggingface.co/..."
        }
      ]
    },
    {
      "title": "Emerging Technologies",
      "key_takeaways": [
        "Quantum AI showing promise",
        "Neuromorphic chips scaling up",
        "Bio-inspired computing gaining traction"
      ],
      "youtube_videos": [
        {
          "title": "Quantum ML Potential",
          "url": "https://youtube.com/watch?v=...",
          "channel": "IBM Research",
          "duration_minutes": 28
        },
        {
          "title": "Neuromorphic Computing Explained",
          "url": "https://youtube.com/watch?v=...",
          "channel": "Intel News",
          "duration_minutes": 16
        }
      ],
      "related_links": [
        {
          "title": "Future of Computing",
          "url": "https://www.mit.edu/..."
        }
      ]
    }
  ],
  "created_at": "2026-03-28T09:00:15Z",
  "source": "scheduler",
  "generated_at": "2026-03-28T09:15:42Z"
}
```

**Response Keys:**
- `_id` (string): Unique MongoDB document ID
- `topic` (string): Research topic
- `summary` (string): Overall summary text
- `topics` (array): Array of 7 topic objects
  - `title` (string): Topic name
  - `key_takeaways` (array): 3 main insights
  - `youtube_videos` (array): 2 video objects
    - `title` (string): Video title
    - `url` (string): YouTube URL
    - `channel` (string): Channel name
    - `duration_minutes` (number): Video length
  - `related_links` (array): Additional resources
    - `title` (string): Link title
    - `url` (string): Full URL
- `created_at` (string): When report was generated (ISO 8601)
- `source` (string): "scheduler" or "api" (who triggered it)
- `generated_at` (string): Exact generation timestamp

**Use Case:** Display latest AI research summary in app

**Error Response (204 No Content):** No report generated yet
```
HTTP 204 No Content
```

---

### 3️⃣ POST `/crew/start`
**Purpose:** Manually trigger new AI research report generation

**Request:**
```bash
curl -X POST https://<your-service-name>.onrender.com/crew/start \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI LLMs, agentic ai, rag, and new ai technology",
    "source": "api"
  }'
```

**Request Body (all optional):**
```json
{
  "topic": "AI LLMs, agentic ai, rag, and new ai technology",
  "source": "api"
}
```

**Response (202 Accepted):**
```json
{
  "message": "Report generation started in background",
  "job_id": "crew_run_1711619415",
  "status": "queued",
  "estimated_time_seconds": 180,
  "poll_status_url": "/status",
  "get_report_url": "/report"
}
```

**Response Keys:**
- `message` (string): Confirmation message
- `job_id` (string): Job identifier
- `status` (string): "queued" or "running"
- `estimated_time_seconds` (number): Expected generation time (usually 180-300 sec)
- `poll_status_url` (string): Endpoint to check progress
- `get_report_url` (string): Endpoint to retrieve when done

**Use Case:** User clicks "Generate Report" in app → Start generation → Poll status

---

### 4️⃣ GET `/status`
**Purpose:** Check current report generation status

**Request:**
```bash
curl https://<your-service-name>.onrender.com/status
```

**Response (200 OK) - While Running:**
```json
{
  "status": "running",
  "message": "Report generation in progress",
  "started_at": "2026-03-28T15:30:00Z",
  "elapsed_seconds": 45,
  "current_phase": "youtube_research",
  "progress_percent": 60,
  "source": "api"
}
```

**Response (200 OK) - Completed:**
```json
{
  "status": "completed",
  "message": "Report generation completed successfully",
  "started_at": "2026-03-28T15:30:00Z",
  "finished_at": "2026-03-28T15:35:42Z",
  "total_seconds": 342,
  "source": "api",
  "report_id": "67f8c3a4b1e9d2f3c5g7h9k0"
}
```

**Response (200 OK) - Failed:**
```json
{
  "status": "failed",
  "message": "Error during YouTube research: API rate limit exceeded",
  "started_at": "2026-03-28T15:30:00Z",
  "error": "API rate limit exceeded",
  "source": "api"
}
```

**Response Keys:**
- `status` (string): "idle", "queued", "running", "completed", "failed"
- `message` (string): Human-readable status
- `started_at` (string): When generation started (ISO 8601)
- `finished_at` (string): When generation finished (only if completed)
- `elapsed_seconds` (number): Time spent so far
- `total_seconds` (number): Total time taken (only if completed)
- `current_phase` (string): "news_research", "youtube_research", "summarization"
- `progress_percent` (number): 0-100% complete
- `source` (string): "scheduler" or "api"
- `error` (string): Error message if failed
- `report_id` (string): MongoDB ID of saved report

**Use Case:** Poll every 5 seconds to show progress bar

---

### 5️⃣ GET `/scheduler/jobs`
**Purpose:** View scheduled jobs configuration

**Request:**
```bash
curl https://<your-service-name>.onrender.com/scheduler/jobs
```

**Response (200 OK):**
```json
{
  "jobs": [
    {
      "id": "daily_report_9am",
      "name": "Daily Report at 9 AM",
      "trigger": "cron[hour=9, minute=0]",
      "timezone": "UTC",
      "next_run": "2026-03-29T09:00:00Z",
      "last_run": "2026-03-28T09:00:15Z",
      "enabled": true
    }
  ],
  "scheduler_active": true,
  "total_jobs": 1
}
```

**Response Keys:**
- `jobs` (array): List of scheduled jobs
  - `id` (string): Job identifier
  - `name` (string): Display name
  - `trigger` (string): Cron expression
  - `timezone` (string): Timezone (UTC)
  - `next_run` (string): Next scheduled execution (ISO 8601)
  - `last_run` (string): Last execution time (ISO 8601)
  - `enabled` (boolean): Is job active?
- `scheduler_active` (boolean): Is scheduler running?
- `total_jobs` (number): Count of scheduled jobs

**Use Case:** Display in app "Next report at: 9:00 AM tomorrow"

---

## Response Schemas

### Report Object
```typescript
interface Report {
  _id: string;                    // MongoDB ID
  topic: string;                  // Research topic
  summary: string;                // Overview text
  topics: Topic[];               // 7 topics
  created_at: string;            // ISO 8601 timestamp
  source: "scheduler" | "api";   // Who triggered
  generated_at: string;          // Generation time
}

interface Topic {
  title: string;                 // Topic name
  key_takeaways: string[];       // 3 insights
  youtube_videos: Video[];       // 2 videos
  related_links: Link[];         // Resources
}

interface Video {
  title: string;                 // Video title
  url: string;                   // YouTube URL
  channel: string;               // Creator channel
  duration_minutes: number;      // Length in minutes
}

interface Link {
  title: string;                 // Link description
  url: string;                   // Full URL
}
```

---

## Examples

### Complete Flow: Generate & Retrieve Report

**Step 1: Trigger Generation**
```bash
curl -X POST https://myapp.onrender.com/crew/start \
  -H "Content-Type: application/json" \
  -d '{"source": "api"}'

# Response:
# {
#   "status": "queued",
#   "estimated_time_seconds": 180
# }
```

**Step 2: Poll Status Every 5 Seconds**
```bash
# First poll (5 sec):
curl https://myapp.onrender.com/status
# {"status": "queued"}

# Second poll (10 sec):
# {"status": "running", "current_phase": "news_research", "progress_percent": 20}

# Third poll (15 sec):
# {"status": "running", "current_phase": "youtube_research", "progress_percent": 40}

# ...keep polling...

# Final poll (180+ sec):
# {"status": "completed", "total_seconds": 342}
```

**Step 3: Get Report**
```bash
curl https://myapp.onrender.com/report

# Response: Full report JSON (see /report section above)
```

### Android Kotlin Example

```kotlin
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

interface AIAgentAPI {
    @GET("/health")
    suspend fun getHealth(): HealthResponse
    
    @GET("/report")
    suspend fun getReport(): Report?
    
    @POST("/crew/start")
    suspend fun startReportGeneration(
        @Body request: GenerateRequest
    ): StartResponse
    
    @GET("/status")
    suspend fun getStatus(): StatusResponse
}

// Create client
val retrofit = Retrofit.Builder()
    .baseUrl("https://myapp.onrender.com")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(AIAgentAPI::class.java)

// Usage
lifecycleScope.launch {
    try {
        // 1. Start generation
        val startResponse = api.startReportGeneration(
            GenerateRequest(source = "api")
        )
        
        // 2. Poll status
        var status: StatusResponse? = null
        repeat(60) { // Try 60 times (5 min max)
            delay(5000) // Wait 5 seconds
            status = api.getStatus()
            if (status?.status == "completed") {
                return@repeat
            }
        }
        
        // 3. Get report
        val report = api.getReport()
        // Display report in UI
        
    } catch (e: Exception) {
        Log.e("APIError", e.message ?: "Unknown error")
    }
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| **200** | OK | Success, use response data |
| **202** | Accepted | Job queued, poll `/status` |
| **204** | No Content | No report exists yet, create one |
| **400** | Bad Request | Invalid input, check JSON format |
| **429** | Too Many Requests | Rate limited, wait 60 sec |
| **500** | Server Error | Retry after 30 sec |
| **503** | Service Unavailable | Temporarily down, retry later |

### Error Response Format

```json
{
  "status": "error",
  "message": "User-friendly error description",
  "error_code": "ERR_RATE_LIMITED",
  "timestamp": "2026-03-28T15:30:00Z"
}
```

### Common Errors & Solutions

#### Error: "Report generation already in progress"
```
Status: 429 Conflict
Message: "Previous generation still running. Check /status"
```
**Solution:** Wait for previous report to complete, then try again

#### Error: "No module named 'crewai'"
```
Status: 500 Internal Server Error
Message: "CrewAI dependency missing"
```
**Solution:** Server issue, retry after 30 seconds

#### Error: "MongoDB connection failed"
```
Status: 503 Service Unavailable
Message: "Cannot save report to database"
```
**Solution:** Temporary connectivity issue, retry after 1 minute. The API now gracefully falls back to file storage if MongoDB is unavailable.

#### Error: "SSL handshake failed" / "TLSV1_ALERT_INTERNAL_ERROR"
```
Status: 500 or 503
Message: "SSL: TLSV1_ALERT_INTERNAL_ERROR"
```
**Solution:** Fixed in v1.1+. The API now:
- Disables strict SSL certificate validation for MongoDB connections
- Uses extended timeouts (10s connect, 30s socket)
- Falls back to file storage if MongoDB is unavailable
- Automatically retries with improved connection parameters

If error persists, verify `MONGODB_URI` is set correctly in environment variables.

---

## Rate Limiting

### Current Limits (Free Tier)
- ✅ No rate limiting on `/health` and `/report`
- ✅ 1 concurrent `/crew/start` job
- ✅ Unlimited `/status` polls

### For Production (Render Standard)
- Same limits with 24/7 uptime

---

## Polling Strategy (Recommended)

```
POST /crew/start
    ↓
Wait 2 seconds (let generation start)
    ↓
GET /status every 5 seconds until:
    - status == "completed" → GET /report
    - status == "failed" → Show error
    - timeout (>10 min) → Manual retry
```

### Recommended UI Flow

```
[Generate Button]
    ↓
Show loading spinner
Progress: Queued...
    ↓
Progress: Running (20%)
Progress: Running (40%)
Progress: Running (60%)
Progress: Running (80%)
    ↓
Progress: Completed ✅
    ↓
[Display Report]
  - 7 Topics
  - Key Takeaways
  - YouTube Videos
  - Related Links
```

---

## MongoDB Schema Reference

Reports are stored with this structure:

```javascript
{
  _id: ObjectId("..."),
  topic: "AI LLMs, agentic ai, rag, and new ai technology",
  summary: "...",
  topics: [
    {
      title: "Large Language Models",
      key_takeaways: ["...", "...", "..."],
      youtube_videos: [
        {
          title: "...",
          url: "...",
          channel: "...",
          duration_minutes: 15
        },
        {...}
      ],
      related_links: [{title: "...", url: "..."}, {...}]
    },
    {...} // 6 more topics
  ],
  created_at: ISODate("2026-03-28T09:00:15.000Z"),
  source: "scheduler",
  generated_at: ISODate("2026-03-28T09:15:42.000Z")
}
```

---

## Testing Checklist

- [ ] Health check responds with 200
- [ ] Report exists (GET /report returns data)
- [ ] Can start new generation (POST /crew/start returns 202)
- [ ] Status updates while running
- [ ] New report saved after generation
- [ ] Stop + restart app → Report still accessible
- [ ] Error handling works (test 500 error)
- [ ] Scheduler job runs daily at 9 AM ✓

---

## Support

For issues:
1. Check `/health` → Is API alive?
2. Check `/status` → Generation failing?
3. View Render logs → Error details
4. Verify MongoDB URI in environment variables

**API is now ready for Android integration!** 🚀
