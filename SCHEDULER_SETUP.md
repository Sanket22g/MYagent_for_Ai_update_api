# Daily Scheduler Setup (9 AM Task Automation)

Your FastAPI server now runs tasks automatically every day at **9:00 AM**.

## How It Works

✅ **Automatic**: Scheduler starts when API server starts
✅ **Daily**: Runs every day at exactly 9:00 AM
✅ **Persistent**: Will run as long as the server is running
✅ **Manageable**: Can pause/resume scheduler via API

---

## Scheduler Endpoints

### View Scheduled Jobs
```bash
curl http://localhost:8000/scheduler/jobs
```

**Response:**
```json
{
  "jobs": [
    {
      "id": "daily_report_9am",
      "name": "Daily Report at 9 AM",
      "trigger": "cron[hour='9', minute='0']",
      "next_run_time": "2026-03-29 09:00:00"
    }
  ],
  "scheduler_running": true
}
```

---

### Pause Scheduler
```bash
curl -X POST http://localhost:8000/scheduler/pause
```

**Response:**
```json
{
  "status": "paused",
  "message": "Scheduler paused"
}
```

---

### Resume Scheduler
```bash
curl -X POST http://localhost:8000/scheduler/resume
```

**Response:**
```json
{
  "status": "resumed",
  "message": "Scheduler resumed"
}
```

---

## Check Scheduled Task Status

```bash
curl http://localhost:8000/status
```

**Response (after 9 AM run):**
```json
{
  "status": "completed",
  "message": "Report generated successfully at 2026-03-28",
  "timestamp": "2026-03-28"
}
```

---

## Server Command

Start the API server (scheduler will auto-start):

```bash
uv run python run_api.py
```

The server will log:
```
[STARTUP] Scheduler started - jobs will run daily at 9:00 AM
[SCHEDULER] Running report generation at 9 AM on 2026-03-28
[SCHEDULER] Report generation completed at 2026-03-28
```

---

## Android Integration with Scheduler

### Check Next Run Time (Kotlin)
```kotlin
val client = OkHttpClient()

val jobsRequest = Request.Builder()
    .url("http://YOUR_SERVER:8000/scheduler/jobs")
    .build()

client.newCall(jobsRequest).execute().use { response ->
    val json = JSONObject(response.body?.string())
    val jobs = json.getJSONArray("jobs")
    val nextRun = jobs.getJSONObject(0).getString("next_run_time")
    
    runOnUiThread {
        findViewById<TextView>(R.id.nextRunText).text = "Next run: $nextRun"
    }
}
```

### Poll Status Until Report is Ready
```kotlin
fun pollReportStatus() {
    val client = OkHttpClient()
    val timer = Timer()
    
    timer.scheduleAtFixedRate(0, 5000) { // Check every 5 seconds
        val statusRequest = Request.Builder()
            .url("http://YOUR_SERVER:8000/status")
            .build()
        
        client.newCall(statusRequest).execute().use { response ->
            val json = JSONObject(response.body?.string())
            val status = json.getString("status")
            
            if (status == "completed") {
                timer.cancel()
                // Fetch the report
                fetchReport()
            } else if (status == "failed") {
                timer.cancel()
                showError("Report generation failed")
            }
        }
    }
}

fun fetchReport() {
    val client = OkHttpClient()
    val reportRequest = Request.Builder()
        .url("http://YOUR_SERVER:8000/report")
        .build()
    
    client.newCall(reportRequest).execute().use { response ->
        val report = JSONObject(response.body?.string())
        // Display report data
    }
}
```

---

## Notes

- **Server must be running** for scheduled tasks to execute
- **Timezone**: Uses your system timezone for 9 AM calculation
- **First Run**: If server starts before 9 AM, it will run at 9 AM the same day
- **Persistence**: If server restarts, scheduler restarts and calculates next 9 AM
- **No Database Required**: Scheduling is in-memory (resets when server restarts)

