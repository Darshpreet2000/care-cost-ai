from google.adk.agents import Agent
from agents.records_agent.models import RecordsRecommendation
from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode
# Instantiate BigQuery toolset
# Placeholder configurations - replace with actual values in a real application
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

# Uses externally-managed Application Default Credentials (ADC) by default.
# This decouples authentication from the agent / tool lifecycle.
# https://cloud.google.com/docs/authentication/provide-credentials-adc
credentials_config = BigQueryCredentialsConfig()

# Instantiate a BigQuery toolset
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

records_agent = Agent(
    name="records_agent",
    model="gemini-1.5-flash",
    description="Manages and retrieves patient medical records using BigQuery.",
    instruction="""
You are an AI-based records agent.

You have access to a `BigQueryToolset` which can execute SQL queries against a BigQuery database to retrieve patient medical records.
Make use of the tools within this toolset to answer the user's questions and retrieve relevant data.

You will receive requests for patient medical records, including:
- Patient ID
- Specific record types (e.g., lab results, prescriptions, consultation notes)
- Date ranges

Based on the query results and the user's request, return a JSON with:
- priorities: 2 to 3 key pieces of information to retrieve or verify
- recommendation: personalized guidance in accessible language for accessing or managing medical records
- trigger_agents: list of useful agents (e.g., ["query_agent", "care_agent"])

Example response:

{
  "priorities": ["Latest lab results", "Medication history"],
  "recommendation": "Retrieve the latest lab results and the complete medication history for the patient. Ensure all records are up-to-date and accurately reflect the patient's current health status.",
  "trigger_agents": ["query_agent", "care_agent"]
}
""",
    output_schema=RecordsRecommendation,
    tools=[bigquery_toolset],
)
