#!/usr/bin/env python
"""Test the /report endpoint for SSL issues"""

import requests
import json

URL = "https://myagent-for-ai-update-api-1.onrender.com"

print("=" * 60)
print("Testing AI Agent API")
print("=" * 60)

# Test /health endpoint
try:
    print("\n1️⃣  Testing /health endpoint...")
    r = requests.get(f"{URL}/health", timeout=15)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ API is healthy!")
        print(f"   Response: {json.dumps(r.json(), indent=2)[:300]}")
    else:
        print(f"   ⚠️  Unexpected status: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test /report endpoint
try:
    print("\n2️⃣  Testing /report endpoint...")
    r = requests.get(f"{URL}/report", timeout=15)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Report retrieved successfully!")
        report_data = r.json()
        print(f"   Topic: {report_data.get('topic', 'N/A')[:80]}")
        print(f"   Summary: {report_data.get('summary', 'N/A')[:80]}")
    elif r.status_code == 404:
        print(f"   ℹ️  No report generated yet (expected)")
    else:
        print(f"   ❌ Error: {r.text[:300]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test /status endpoint
try:
    print("\n3️⃣  Testing /status endpoint...")
    r = requests.get(f"{URL}/status", timeout=15)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Status retrieved!")
        print(f"   Response: {json.dumps(r.json(), indent=2)[:300]}")
    else:
        print(f"   ⚠️  Error: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
