from pydantic import BaseModel
from typing import List

class FinanceRecommendation(BaseModel):
    priorities: List[str]
    recommendation: str
    trigger_agents: List[str]
