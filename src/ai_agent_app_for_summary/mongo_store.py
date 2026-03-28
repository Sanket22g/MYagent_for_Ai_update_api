from __future__ import annotations

import os
import ssl
from datetime import datetime, timezone
from typing import Any

from pymongo import DESCENDING, MongoClient

DEFAULT_DB_NAME = "ai_agent_app"
DEFAULT_COLLECTION = "reports"


def _get_collection():
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        print("❌ MONGODB_URI not set")
        return None

    # Build SSL/TLS options for MongoDB connection
    ssl_options = {
        # Disable SSL certificate validation (required for some environments)
        "ssl_cert_reqs": ssl.CERT_NONE,
        # Allow invalid certificates
        "ssl_match_hostname": False,
        # Increase timeouts
        "serverSelectionTimeoutMS": 10000,
        "connectTimeoutMS": 10000,
        "socketTimeoutMS": 30000,
        # Disable socket keep-alive to avoid stale connections
        "socketKeepAliveMS": 30000,
    }

    try:
        print(f"🔌 Connecting to MongoDB with SSL/TLS overrides...")
        
        # Create client with SSL options
        client = MongoClient(
            mongo_uri,
            **ssl_options,
            retryWrites=False,  # Disable retry writes on SSL issues
            uuidRepresentation="standard",
        )
        
        # Test connection
        client.admin.command("ping")
        print("✅ MongoDB connected successfully")
        
        db_name = os.getenv("MONGODB_DB", DEFAULT_DB_NAME)
        collection_name = os.getenv("MONGODB_COLLECTION", DEFAULT_COLLECTION)
        return client[db_name][collection_name]
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return None


def save_report(report: dict[str, Any], source: str) -> str | None:
    collection = _get_collection()
    if collection is None:
        print(f"⚠️  MongoDB unavailable, skipping MongoDB save (will use file storage)")
        return None

    try:
        payload = {
            "source": source,
            "report": report,
            "created_at": datetime.now(timezone.utc),
        }
        inserted = collection.insert_one(payload)
        print(f"✅ Report saved to MongoDB: {inserted.inserted_id}")
        return str(inserted.inserted_id)
    except Exception as e:
        print(f"⚠️  Failed to save report to MongoDB: {e}")
        print(f"   Will use file storage instead")
        return None


def get_latest_report() -> dict[str, Any] | None:
    collection = _get_collection()
    if collection is None:
        return None

    doc = collection.find_one(sort=[("created_at", DESCENDING)])
    if not doc:
        return None

    report = doc.get("report")
    return report if isinstance(report, dict) else None
