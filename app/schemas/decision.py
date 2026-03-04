from pydantic import BaseModel
from typing import Optional


# ---- Request Schema ----
class DecisionRequest(BaseModel):
    text: str


# ---- Response Schema ----
class DecisionResponse(BaseModel):
    decision_id: int
    predicted_label: str
    confidence_score: float
    model_version: str


# ---- Review Request ----
class ReviewRequest(BaseModel):
    reviewer_name: str
    overridden_label: Optional[str] = None
    comments: Optional[str] = None


class ReviewResponse(BaseModel):
    review_id: int
    decision_id: int
    reviewer_name: str
    overridden_label: Optional[str]
    comments: Optional[str]