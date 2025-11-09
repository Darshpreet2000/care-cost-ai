from google.adk.agents.sequential_agent import SequentialAgent
from agents.intake_agent.agent import intake_agent
from agents.query_agent.agent import query_agent
from agents.records_agent.agent import records_agent
from agents.finance_agent.agent import finance_agent
from agents.care_agent.agent import care_agent
from agents.insight_agent.agent import insight_agent

workflow = SequentialAgent(
    name="MediCompareAIWorkflow",
    sub_agents=[
        intake_agent, query_agent, records_agent,
        finance_agent, care_agent, insight_agent
    ]
)
