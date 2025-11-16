from pydantic import BaseModel
from typing import List

class RecordsRecommendation(BaseModel):
    user_chat_message: List[str]
