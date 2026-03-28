#!/usr/bin/env python
"""Start the FastAPI server"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "ai_agent_app_for_summary.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
