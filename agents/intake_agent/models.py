# intake_recommendation.py

from pydantic import BaseModel, Field
from typing import Literal


class IntakeRecommendation(BaseModel):
    """
    Structured output returned by the Intake Agent ("Nurse Clara").
    This model enforces the two allowed output states:
    - handoff_to_dr_leo
    - pending_clarification
    """

    status: Literal["handoff_to_dr_leo", "pending_clarification"] = Field(
        ...,
        description="Determines whether the workflow continues or requests clarification."
    )

    # SUCCESS FIELDS ----------------------------------------------------
    procedure_name_confirmed: str | None = Field(
        None,
        description="Confirmed name of the medical procedure. Required for success."
    )
    location_confirmed: str | None = Field(
        None,
        description="Confirmed location (state or metro). Required for success."
    )
    insurance_context_notes: str | None = Field(
        None,
        description="Insurance details if provided by the user, otherwise 'N/A'."
    )

    # PENDING FIELDS ----------------------------------------------------
    clarification_question: str | None = Field(
        None,
        description="A single clarifying question when mandatory attributes are missing."
    )
    missing_attributes: str | None = Field(
        None,
        description="Comma-separated list of missing attributes: Procedure, Location, or both."
    )
    user_chat_response: str | None = Field(
        None,
        description="Your response to user chatting in the intake process."
    )
