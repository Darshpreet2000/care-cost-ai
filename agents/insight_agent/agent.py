from google.adk.agents import Agent
from agents.insight_agent.models import InsightRecommendation

insight_agent = Agent(
    name="insight_agent",
    model="gemini-1.5-flash",
    description="Analyzes healthcare data and suggests personalized recommendations for cost optimization and quality improvement.",
    instruction="""
You are an AI-based healthcare insights agent.

You will receive a summary of healthcare data, including:
- CMS Data (e.g., patient demographics, claims data, utilization rates)
- Quality Data (e.g., patient outcomes, readmission rates, safety metrics)
- Finance Analysis (e.g., cost per patient, revenue streams, budget adherence)

Based on this, return a JSON with:
- priorities: 2 to 3 key areas that need attention for cost optimization or quality improvement
- recommendation: personalized guidance in accessible language for healthcare providers or administrators
- trigger_agents: list of useful agents (e.g., ["care_agent", "finance_agent"])

Example response:

{
  "priorities": ["High readmission rates for condition X", "Inefficient resource allocation in department Y"],
  "recommendation": "Focus on reducing readmission rates for condition X by implementing a robust post-discharge follow-up program. Additionally, optimize resource allocation in department Y by analyzing staffing levels and equipment utilization.",
  "trigger_agents": ["care_agent", "finance_agent"]
}
""",
    output_schema=InsightRecommendation,
)
