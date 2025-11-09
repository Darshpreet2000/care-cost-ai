from pydantic import BaseModel
from typing import List

class CareRecommendation(BaseModel):
    priorities: List[str]
    recommendation: str
    trigger_agents: List[str]
