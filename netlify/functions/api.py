from mangum import Mangum
import os
import sys

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
if SRC_DIR not in sys.path:
	sys.path.append(SRC_DIR)

from ai_agent_app_for_summary.api import app

# Netlify/AWS Lambda entry point
handler = Mangum(
	app,
	lifespan="off",
	api_gateway_base_path="/.netlify/functions/api",
)
