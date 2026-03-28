# AI Agent App Summary API

FastAPI server for generating AI research summary reports with YouTube videos.

## Quick Start

### 1. Start the API Server

```bash
uv run python run_api.py
```

Or:

```bash
uv run uvicorn ai_agent_app_for_summary.api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### 2. API Endpoints

#### **GET /health**
Health check endpoint.

```
GET http://localhost:8000/health
```

Response:
```json
{"status": "healthy"}
```

---

#### **POST /generate**
Generate a new report (runs in background).

```
POST http://localhost:8000/generate?topic=AI%20LLMs%20and%20RAG
```

Query Parameters:
- `topic` (optional): Search topic (default: "AI LLMs, agentic ai, rag, and new ai technology")

Response:
```json
{
  "status": "started",
  "message": "Report generation started in background",
  "topic": "AI LLMs and RAG"
}
```

---

#### **GET /status**
Check report generation status.

```
GET http://localhost:8000/status
```

Response:
```json
{
  "status": "completed",
  "message": "Report generated successfully"
}
```

Possible statuses: `idle`, `generating`, `running`, `completed`, `failed`

---

#### **GET /report**
Get the latest generated report.

```
GET http://localhost:8000/report
```

Response: Full JSON report with 7 AI topics, summaries, and YouTube videos.

---

## API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Android Integration Example

### Kotlin
```kotlin
val client = OkHttpClient()

// 1. Trigger report generation
val generateRequest = Request.Builder()
    .url("http://YOUR_SERVER:8000/generate?topic=AI%20LLMs")
    .post(RequestBody.create(null, byteArrayOf()))
    .build()

client.newCall(generateRequest).execute().use { response ->
    Log.d("API", response.body?.string())
}

// 2. Check status
val statusRequest = Request.Builder()
    .url("http://YOUR_SERVER:8000/status")
    .build()

client.newCall(statusRequest).execute().use { response ->
    val json = response.body?.string()
    Log.d("Status", json)
}

// 3. Get report when ready
val reportRequest = Request.Builder()
    .url("http://YOUR_SERVER:8000/report")
    .build()

client.newCall(reportRequest).execute().use { response ->
    val report = JSONObject(response.body?.string())
    // Parse and display topics, videos, etc.
}
```

---

## Environment Variables

Add to `.env` if needed:

```
YOUTUBE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```

---

## Notes

- The `/generate` endpoint runs asynchronously in the background
- Poll `/status` to check progress
- Report is saved to `final_report.json` after completion
- First request takes longer (typically 2-5 minutes) due to API calls

