from pydantic import BaseModel
from typing import List

class InsightRecommendation(BaseModel):
    markdown_report: str
    user_chat_message: str
