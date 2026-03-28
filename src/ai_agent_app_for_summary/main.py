#!/usr/bin/env python
import warnings
from datetime import date, timedelta
from pathlib import Path

from ai_agent_app_for_summary.crew import AiAgentAppForSummary
from ai_agent_app_for_summary.report_normalizer import normalize_report_file

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    today = date.today()
    two_days_ago = today - timedelta(days=2)
    
    inputs = {
        'topic': 'AI LLMsAI LLMs, agentic ai , rag,and new ai technology',
        'date': today.strftime("%m/%d/%Y"),
        'two_days_ago': two_days_ago.strftime("%m/%d/%Y")
    }

    try:
        AiAgentAppForSummary().crew().kickoff(inputs=inputs)
        report_file = Path(__file__).parent.parent.parent / "final_report.json"
        if report_file.exists():
            normalize_report_file(report_file)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()