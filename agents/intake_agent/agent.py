from google.adk.agents import Agent
from agents.intake_agent.models import IntakeRecommendation

intake_agent = Agent(
    name="intake_agent",
    model="gemini-1.5-flash",
    description="Gathers initial patient information and identifies key concerns.",
    instruction="""
You are an AI-based intake agent.

You will receive initial patient information, including:
- Demographics
- Chief complaint
- Brief medical history
- Current medications

Based on this, return a JSON with:
- priorities: 2 to 3 key concerns or areas for further investigation
- recommendation: personalized guidance in accessible language for the next steps in patient care
- trigger_agents: list of useful agents (e.g., ["query_agent", "records_agent"])

Example response:

{
  "priorities": ["Acute pain management", "Medication reconciliation"],
  "recommendation": "Prioritize acute pain management and ensure a thorough medication reconciliation to avoid adverse drug interactions. Consider consulting a pain specialist.",
  "trigger_agents": ["query_agent", "records_agent"]
}
""",
    output_schema=IntakeRecommendation,
)
