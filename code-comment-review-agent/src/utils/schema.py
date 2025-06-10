from pydantic import BaseModel
from typing import List

class CodeReviewSchema(BaseModel):
    """Schema for representing code review results.
    
    Attributes:
        score: Numeric rating of the code quality (typically 1-10 or 1-100).
        feedback: List of textual feedback items about the code.
        suggestions: List of suggested improvements for the code.
        strengths: List of positive aspects found in the code.
    """
    score: int
    feedback: List[str]
    suggestions: List[str]
    strengths: List[str]