from pydantic import BaseModel
from typing import List

class CareRecommendation(BaseModel):
    user_chat_message: List[str]
 