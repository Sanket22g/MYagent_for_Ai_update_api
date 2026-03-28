from mangum import Mangum

from ai_agent_app_for_summary.api import app

# Netlify/AWS Lambda entry point
handler = Mangum(app, lifespan="off")
