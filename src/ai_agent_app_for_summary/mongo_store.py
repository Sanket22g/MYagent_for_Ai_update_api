from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from pymongo import DESCENDING, MongoClient

DEFAULT_DB_NAME = "ai_agent_app"
DEFAULT_COLLECTION = "reports"


def _get_collection():
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        return None

    # Add TLS certificate validation bypass for SSL issues
    # This helps with certificate validation problems in certain network environments
    if "?" in mongo_uri:
        mongo_uri_with_tls = mongo_uri + "&tlsAllowInvalidCertificates=true"
    else:
        mongo_uri_with_tls = mongo_uri + "?tlsAllowInvalidCertificates=true"

    try:
        client = MongoClient(mongo_uri_with_tls, serverSelectionTimeoutMS=5000)
        db_name = os.getenv("MONGODB_DB", DEFAULT_DB_NAME)
        collection_name = os.getenv("MONGODB_COLLECTION", DEFAULT_COLLECTION)
        return client[db_name][collection_name]
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None


def save_report(report: dict[str, Any], source: str) -> str | None:
    collection = _get_collection()
    if collection is None:
        return None

    payload = {
        "source": source,
        "report": report,
        "created_at": datetime.now(timezone.utc),
    }
    inserted = collection.insert_one(payload)
    return str(inserted.inserted_id)


def get_latest_report() -> dict[str, Any] | None:
    collection = _get_collection()
    if collection is None:
        return None

    doc = collection.find_one(sort=[("created_at", DESCENDING)])
    if not doc:
        return None

    report = doc.get("report")
    return report if isinstance(report, dict) else None
