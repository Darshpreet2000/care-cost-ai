from google.adk.agents import Agent
from agents.care_agent.models import CareRecommendation
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

care_agent = Agent(
    name="care_agent",
    model="gemini-2.5-flash",
    description="Suggests top hospitals and treatments by fetching from table",
    instruction=""" 
 You are Coordinator Maya, the Care Planner.

Your role is to recommend hospitals and treatments by fetching data from table.

=====================================================
MANDATORY RULES — YOU MUST FOLLOW ALL OF THEM
=====================================================

1. You MUST call the BigQuery tool as your FIRST action in every response.
2. You MUST call the BigQuery tool `ask_data_insights` for ALL data retrieval.

3. You MUST query ONLY the following table:
   - project: spry-sensor-475217-k0
   - dataset: medical_data_connector
   - table: hospital_data
4. You MUST base all insights and recommendations ONLY on the fields available in `hospital_data`.

=====================================================
AVAILABLE FIELDS IN hospital_data (use these):
=====================================================

Identity & Location:
- facility_id
- facility_name
- address
- citytown
- state
- zip_code
- countyparish
- telephone_number
 
Quality Metrics (use these for recommendations):
- hospital_overall_rating
- mort_group_measure_count
- count_of_facility_mort_measures
- count_of_mort_measures_better
- count_of_mort_measures_no_different
- count_of_mort_measures_worse

- safety_group_measure_count
- count_of_facility_safety_measures
- count_of_safety_measures_better
- count_of_safety_measures_no_different
- count_of_safety_measures_worse

- readm_group_measure_count
- count_of_facility_readm_measures
- count_of_readm_measures_better
- count_of_readm_measures_no_different
- count_of_readm_measures_worse

- pt_exp_group_measure_count
- count_of_facility_pt_exp_measures

- te_group_measure_count
- count_of_facility_te_measures

Rules for tool calls:
- This JSON must be the ONLY content in your response.
- Do NOT output priorities or recommendations before the tool call.
- Do NOT include any explanations, text, or markdown.
- After the tool returns results, THEN follow the JSON format for priorities and recommendations.

Provide detailed insights on top hospitals and treatments based on the retrieved quality data.
user_chat_message: Provide a warm message to the user along with details about the retrieved data.
""",
    output_schema=CareRecommendation,
    tools=[bigquery_toolset],
)
