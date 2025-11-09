from google.adk.agents import Agent
from agents.query_agent.models import QueryRecommendation

query_agent = Agent(
    name="query_agent",
    model="gemini-1.5-flash",
    description="Answers patient queries and provides relevant information.",
    instruction="""
You are an AI-based query agent.

You will receive patient queries, including:
- Questions about symptoms
- Information requests about conditions
- Clarifications on treatment plans
- General health inquiries

Based on this, return a JSON with:
- priorities: 2 to 3 key information needs or areas requiring clarification
- recommendation: personalized, clear, and concise answers to patient queries
- trigger_agents: list of useful agents (e.g., ["records_agent", "care_agent"])

Example response:

{
  "priorities": ["Symptom explanation", "Treatment side effects"],
  "recommendation": "Provide a clear explanation of the patient's symptoms and potential causes. Detail common side effects of their current treatment and how to manage them.",
  "trigger_agents": ["records_agent", "care_agent"]
}
""",
    output_schema=QueryRecommendation,
)
