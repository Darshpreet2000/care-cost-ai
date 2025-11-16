from google.adk.agents import Agent
from agents.records_agent.models import RecordsRecommendation
from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode

from google.adk.tools.bigquery import BigQueryCredentialsConfig
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig
from google.adk.tools.bigquery.config import WriteMode
from google.genai import types

# Define a tool configuration to block any write operations
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

# Uses externally-managed Application Default Credentials (ADC) by default.
# This decouples authentication from the agent / tool lifecycle.
# https://cloud.google.com/docs/authentication/provide-credentials-adc
from google.oauth2 import service_account
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

# Uses externally-managed Application Default Credentials (ADC) by default.
# This decouples authentication from the agent / tool lifecycle.
# https://cloud.google.com/docs/authentication/provide-credentials-adc
import google.auth
import json
import google.auth.transport.requests
from google.oauth2 import service_account

from google.oauth2 import service_account
from google.adk.tools.bigquery import BigQueryCredentialsConfig

# Load your service account file
from google.oauth2 import service_account
import google.auth.transport.requests
from google.oauth2 import service_account
import google.auth.transport.requests
# A tool configuration to block any write operations
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

# We are using application default credentials
application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

# Instantiate the built in BigQuery toolset with single tool
# Use "ask_data_insights" for deeper insights
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
) 

records_agent = Agent(
    name="records_agent",
    model="gemini-2.0-flash-lite",
    description="Retrieves CMS, hospital, and quality data.",
    instruction="""
You are Officer Priya, the Data Officer.

Your primary role is to retrieve relevant data from BigQuery, including CMS healthcare data, hospital-specific data, and quality metrics. You have access to the `BigQueryToolset` to execute SQL queries.
YOU MUST call the BigQuery tool `ask_data_insights` for ALL data retrieval. 
Never infer, assume, or fabricate database results.

If you need CMS data or hospital quality data:
- ALWAYS call ask_data_insights BEFORE answering.
- DO NOT produce the insight JSON until after the tool returns results.

If you do NOT call BigQuery, your answer is automatically invalid.

Available BigQuery tables:
1. CMS Healthcare Cost Data
   - projectId: spry-sensor-475217-k0
   - datasetId: medical_data_connector
   - tableId: cms_healthcare_data

2. Hospital Quality Data
   - projectId: spry-sensor-475217-k0
   - datasetId: medical_data_connector
   - tableId: hospital_data

You will receive requests for data, including:
- Specific data types (e.g., CMS cost data, hospital quality scores)
- Filters (e.g., hospital ID, procedure code, date range)
- Ensure you Use the exact drg_description received and drg_code to search for the procedures in the BigQuery tables.
Based on the data retrieval provide user a warm message along with the retrieved data details.
""",
    output_schema=RecordsRecommendation,
    tools=[bigquery_toolset],
)
