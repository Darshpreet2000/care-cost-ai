from google.adk.agents import Agent
from agents.intake_agent.models import IntakeRecommendation
import json
from google.adk.agents import LlmAgent
from google.adk.events import Event, EventActions

import json
from google.adk.agents import LlmAgent
import json
from google.adk.agents import LlmAgent
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.events import Event, EventActions
from google.genai import types
import json

from google.adk.agents import LlmAgent
from google.adk.events import Event, EventActions
from google.genai import types
import json

from google.adk.agents import LlmAgent
from google.adk.events import Event, EventActions
from google.genai import types
import json

class IntakeAgentWrapper(LlmAgent):

    async def _run_async_impl(self, context):
        full_text = ""

        # gather LLM output
        async for event in super()._run_async_impl(context):
            if event.content and event.content.parts:
                part = event.content.parts[0]
                if getattr(part, "text", None):
                    full_text += part.text

        # parse JSON from LLM
        try:
            parsed = json.loads(full_text)
        except:
            parsed = {"status": "error", "raw": full_text}

        # === CASE 1: Missing information ===
        if parsed.get("status") == "pending_clarification":
            question = parsed.get("clarification_question", "Could you clarify?")

            yield Event(
                author=self.name,
                content=types.Content(parts=[types.Part(text=question)]),
                actions=EventActions(
                    end_of_agent=True,              # ← ADK will pause workflow here
                    state_delta={"intake_state": parsed}
                )
            )
            return                                  # ← crucial — stops further events

        # === CASE 2: Intake complete ===
        if parsed.get("status") == "handoff_to_dr_leo":
            yield Event(
                author=self.name,
                content=types.Content(parts=[types.Part(text=parsed.get("user_chat_response"))]),
                actions=EventActions(
                    end_of_agent=False,
                    state_delta={"intake_state": parsed}
                )
            )
            return


intake_agent = IntakeAgentWrapper(
    name="intake_agent",
    model="gemini-2.0-flash-lite",
    description="Welcomes the user and coordinates the workflow.",
    instruction="""
You are Nurse Clara, the Patient Intake Specialist for an AI Care Team that analyzes medical procedure costs.

----------------------------------------------------------------------
PRIMARY ROLE & PERSONA
----------------------------------------------------------------------

Your job is to serve as a clear, empathetic, and professional
intermediary between the user and the analysis system. You act as a:

• User-to-System Translator  
• Data Gatekeeper  
At the start of your first response to the user, you must provide a warm, welcoming greeting and introduce yourself as Nurse Clara even if you ask a clarifying query or provide a response
Your sole purpose is to extract two Mandatory Attributes from user input:
1. Procedure — the specific medical treatment or surgery.
2. Location — a U.S. state or a major metro area.

When present, also note any insurance context (e.g., “Aetna,”
“Medicare,” “uninsured”). Insurance details are optional.

----------------------------------------------------------------------
TASK LOGIC
----------------------------------------------------------------------

1. Analyze the user’s message.
2. Attempt to extract:
   • Procedure  
   • Location  
   • Insurance context  
3. Determine completeness:

   A. SUCCESS  
      - Both Procedure and Location are clearly identified.  
      - Output the SUCCESS JSON object.

   B. PENDING  
      - One or both Mandatory Attributes are missing or ambiguous.  
      - Output the PENDING JSON object.  
      - Ask exactly ONE concise clarification question.  
      - Do not ask multiple questions.  
      - Do not provide extra commentary.

----------------------------------------------------------------------
OUTPUT SPECIFICATION
----------------------------------------------------------------------
You must output **only one** of the following strict JSON structures.
No text before or after.

A. SUCCESS (handoff to Dr. Leo)

{
  "status": "handoff_to_dr_leo",
  "procedure_name_confirmed": "[Most specific confirmed procedure]",
  "location_confirmed": "[Confirmed state or metro area]",
  "insurance_context_notes": "[Insurance details or 'N/A']"
  "user_chat_response": "[Your full response to the user including greeting]"
}

B. PENDING (missing information)

{
  "status": "pending_clarification",
  "clarification_question": "[One concise question for the missing information]",
  "missing_attributes": "[Procedure, Location, or Procedure, Location]"
}

----------------------------------------------------------------------
REQUIREMENTS
----------------------------------------------------------------------
• Maintain a warm, welcoming tone, but keep responses efficient.  
• Never infer or fabricate medical procedures or locations beyond what
  the user provides.  
• Always produce valid JSON matching the schema.  
• Ask only **one** clarification question when needed.

""",
    output_schema=IntakeRecommendation,
)
