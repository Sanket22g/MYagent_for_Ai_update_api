#!/usr/bin/env python
"""FastAPI server for AI Agent App Summary"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from datetime import date, datetime, timedelta
import json
import os
from pathlib import Path
from threading import Lock

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from ai_agent_app_for_summary.crew import AiAgentAppForSummary
from ai_agent_app_for_summary.mongo_store import get_latest_report, save_report
from ai_agent_app_for_summary.report_normalizer import normalize_report_file, normalize_report_payload

app = FastAPI(
    title="AI Agent App Summary API",
    description="API to generate AI research summary reports",
    version="1.0.0"
)

# Store for report status
report_status = {
    "status": "idle",
    "message": "No report generated yet",
    "source": None,
    "started_at": None,
    "finished_at": None,
    "storage": {"type": "file", "id": None},
}
report_file = Path(__file__).parent.parent.parent / "final_report.json"

# Scheduler
scheduler = BackgroundScheduler()
scheduler_running = False
run_lock = Lock()

DEFAULT_TOPIC = "AI LLMs, agentic ai, rag, and new ai technology"


def _normalize_from_crew_result(result) -> dict:
    """Normalize report directly from crew result when possible."""
    # Try structured dict-like output first.
    if hasattr(result, "json_dict") and isinstance(result.json_dict, dict):
        return normalize_report_payload(result.json_dict)

    # Fallback to parsing raw text as JSON.
    raw = getattr(result, "raw", None)
    if isinstance(raw, str):
        try:
            return normalize_report_payload(json.loads(raw))
        except Exception:
            pass

    # Last-resort fallback shape.
    return normalize_report_payload({})


def _run_crew_job(topic: str, source: str):
    """Run crew and normalize report. Source is 'manual' or 'scheduled'."""
    global report_status

    if not run_lock.acquire(blocking=False):
        report_status = {
            "status": "busy",
            "message": "Crew is already running",
            "source": source,
            "started_at": None,
            "finished_at": None,
        }
        return

    started_at = datetime.utcnow().isoformat()
    storage_info = {"type": "file", "id": None}
    try:
        today = date.today()
        two_days_ago = today - timedelta(days=2)

        inputs = {
            "topic": topic,
            "date": today.strftime("%m/%d/%Y"),
            "two_days_ago": two_days_ago.strftime("%m/%d/%Y"),
        }

        report_status = {
            "status": "running",
            "message": "Crew execution in progress",
            "source": source,
            "started_at": started_at,
            "finished_at": None,
        }

        result = AiAgentAppForSummary().crew().kickoff(inputs=inputs)

        normalized_report = _normalize_from_crew_result(result)
        inserted_id = save_report(normalized_report, source=source)
        if inserted_id:
            storage_info = {"type": "mongodb", "id": inserted_id}
        elif report_file.exists():
            # Keep backward-compat fallback for local runs.
            normalized_report = normalize_report_file(report_file)

        report_status = {
            "status": "completed",
            "message": "Report generated successfully",
            "source": source,
            "started_at": started_at,
            "finished_at": datetime.utcnow().isoformat(),
            "storage": storage_info,
        }
    except Exception as e:
        report_status = {
            "status": "failed",
            "message": str(e),
            "source": source,
            "started_at": started_at,
            "finished_at": datetime.utcnow().isoformat(),
            "storage": storage_info,
        }
    finally:
        run_lock.release()


def scheduled_report_generation():
    """Generate report at scheduled time"""
    _run_crew_job(DEFAULT_TOPIC, source="scheduled")


@app.on_event("startup")
async def startup_event():
    """Start scheduler on app startup"""
    global scheduler_running
    # Disable scheduler on serverless platforms (Netlify Functions, AWS Lambda, etc.)
    # Enable on traditional web services (Render, Heroku, etc.)
    if os.getenv("NETLIFY") or os.getenv("DISABLE_SCHEDULER", "").lower() == "true":
        return

    if not scheduler_running:
        # Schedule job to run daily at 9:00 AM
        scheduler.add_job(
            scheduled_report_generation,
            CronTrigger(hour=9, minute=0),
            id='daily_report_9am',
            name='Daily Report at 9 AM'
        )
        scheduler.start()
        scheduler_running = True
        print("[STARTUP] Scheduler started - jobs will run daily at 9:00 AM")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop scheduler on app shutdown"""
    global scheduler_running
    if scheduler_running:
        scheduler.shutdown()
        scheduler_running = False
        print("[SHUTDOWN] Scheduler stopped")


@app.get("/")
async def root():
    """Root endpoint - API info"""
    return {
        "name": "AI Agent App Summary API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "This endpoint",
            "GET /health": "Health check",
            "GET /report": "Get latest report",
            "POST /crew/start": "Start crew (for app button)",
            "POST /generate": "Alias for /crew/start",
            "GET /status": "Check crew run status",
            "GET /scheduler/jobs": "Daily schedule info",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/fetch")
async def fetch_from_mongodb():
    """Fetch latest report directly from MongoDB"""
    try:
        from pymongo import MongoClient
        import os
        
        mongo_uri = os.getenv("MONGODB_URI")
        if not mongo_uri:
            raise HTTPException(status_code=500, detail="MongoDB URI not configured")
        
        # Add TLS options for SSL certificate handling
        if "?" in mongo_uri:
            mongo_uri = mongo_uri + "&tlsAllowInvalidCertificates=true"
        else:
            mongo_uri = mongo_uri + "?tlsAllowInvalidCertificates=true"
        
        # Connect with timeout
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client[os.getenv("MONGODB_DB", "ai_agent_app")]
        collection = db[os.getenv("MONGODB_COLLECTION", "reports")]
        
        # Get latest report
        doc = collection.find_one(sort=[("created_at", -1)])
        
        if not doc:
            raise HTTPException(status_code=404, detail="No reports found in MongoDB")
        
        report = doc.get("report", {})
        return {
            "success": True,
            "source": "mongodb",
            "report": report,
            "metadata": {
                "id": str(doc["_id"]),
                "created_at": str(doc["created_at"]),
                "source": doc.get("source", "unknown")
            }
        }
        
    except Exception as e:
        error_msg = str(e)
        return {
            "success": False,
            "error": error_msg[:200],
            "message": "Failed to fetch from MongoDB. Check connection and credentials."
        }


@app.get("/report")
async def get_report():
    """Get the latest generated report"""
    try:
        # Try MongoDB first
        try:
            mongo_report = get_latest_report()
            if mongo_report is not None:
                print("✅ Report retrieved from MongoDB")
                return mongo_report
        except Exception as mongo_error:
            print(f"⚠️  MongoDB read failed, falling back to file: {mongo_error}")

        # Fallback to file storage
        if not report_file.exists():
            raise HTTPException(status_code=404, detail="No report generated yet. Call /crew/start first.")

        print("📄 Report retrieved from file storage")
        return normalize_report_file(report_file)
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error reading report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading report: {str(e)}")


@app.post("/crew/start")
async def start_crew(background_tasks: BackgroundTasks, topic: str = DEFAULT_TOPIC):
    """Start crew manually. Use this endpoint from a single app button."""
    global report_status

    if run_lock.locked():
        return {
            "status": "busy",
            "message": "Crew is already running",
            "topic": topic,
        }

    report_status = {
        "status": "queued",
        "message": "Manual run queued",
        "source": "manual",
        "started_at": None,
        "finished_at": None,
    }
    background_tasks.add_task(_run_crew_job, topic, "manual")

    return {
        "status": "started",
        "message": "Crew started in background",
        "topic": topic,
        "source": "manual",
    }


@app.post("/generate")
async def generate_report_alias(background_tasks: BackgroundTasks, topic: str = DEFAULT_TOPIC):
    """Backward-compatible alias."""
    return await start_crew(background_tasks, topic)


@app.get("/status")
async def get_status():
    """Get current report generation status"""
    return report_status


@app.get("/scheduler/jobs")
async def get_scheduler_jobs():
    """Get all scheduled jobs"""
    if not scheduler_running:
        return {"error": "Scheduler not running"}
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "trigger": str(job.trigger),
            "next_run_time": str(job.next_run_time)
        })
    
    return {"jobs": jobs, "scheduler_running": scheduler_running}


@app.post("/scheduler/pause")
async def pause_scheduler():
    """Pause the scheduler"""
    global scheduler_running
    if scheduler_running:
        scheduler.pause()
        return {"status": "paused", "message": "Scheduler paused"}
    return {"status": "error", "message": "Scheduler not running"}


@app.post("/scheduler/resume")
async def resume_scheduler():
    """Resume the scheduler"""
    if scheduler_running:
        scheduler.resume()
        return {"status": "resumed", "message": "Scheduler resumed"}
    return {"status": "error", "message": "Scheduler not running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
