from pydantic import BaseModel
from typing import List

class RecordsRecommendation(BaseModel):
    priorities: List[str]
    recommendation: str
    trigger_agents: List[str]
