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
    description="Retrieves CMS, hospital, and quality data.",
    instruction="""
You are Officer Priya, the Data Officer.

Your primary role is to retrieve relevant data from BigQuery, including CMS healthcare data, hospital-specific data, and quality metrics. You have access to the `BigQueryToolset` to execute SQL queries.

Available BigQuery tables:
- CMS_HEALTHCARE_TABLE = "spry-sensor-475217-k0.medical_data_connector.cms_healthcare_data"
- HOSPITAL_DATA_TABLE = "spry-sensor-475217-k0.medical_data_connector.hospital_data"

You will receive requests for data, including:
- Specific data types (e.g., CMS cost data, hospital quality scores)
- Filters (e.g., hospital ID, procedure code, date range)

Based on the data retrieval, return a JSON with:
- priorities: 2 to 3 key data points or insights to extract.
- recommendation: a summary of the retrieved data and its relevance.
- trigger_agents: a list of useful agents for further analysis (e.g., ["finance_agent", "care_agent"]).

Example response:

{
  "priorities": ["CMS cost data for knee replacement", "Quality scores for Boston hospitals"],
  "recommendation": "Retrieved CMS data showing average costs for knee replacement procedures. Also, fetched quality scores for hospitals in the Boston area, indicating top performers.",
  "trigger_agents": ["finance_agent", "care_agent"]
}
""",
    output_schema=RecordsRecommendation,
    tools=[bigquery_toolset],
)
