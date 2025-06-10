from pydantic import BaseModel
from typing import List

class CodeReviewSchema(BaseModel):
    score: int
    feedback: List[str]
    suggestions: List[str]
    strengths: List[str]
