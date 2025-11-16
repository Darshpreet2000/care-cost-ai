from pydantic import BaseModel
from typing import List

class QueryRecommendation(BaseModel):
    procedure: str
    drg_code: str
    drg_description: str
    cpt_codes: list[str]
    justification: str
    user_chat_message: str
