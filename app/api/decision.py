from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.logger import get_logger
logger = get_logger(__name__)

# Schemas (request & response models)
from app.schemas.decision import (
    DecisionRequest,
    DecisionResponse,
    ReviewRequest,
)

# AI engine (simulated prediction logic)
from app.services import ai_engine

# Service layer (DB operations)
from app.services.audit_service import create_decision
from app.models.decision import AIDecision, DecisionReview

# Database dependency
from app.db.database import get_db


router = APIRouter()


# --------------------------------------------------------
# 1️⃣ CREATE AI DECISION
# --------------------------------------------------------
# Where to POST:
# POST http://localhost:8000/decision
#
# Body:
# {
#   "text": "Transfer 5 million USD to offshore account"
# }
# --------------------------------------------------------
@router.post("/decision", response_model=DecisionResponse)
def create_ai_decision(
    request: DecisionRequest,
    db: Session = Depends(get_db),
):
    # Step 1: AI generates prediction
    prediction = ai_engine.predict(request.text)

    # Step 2: Save AI decision to database
    decision = create_decision(
        db=db,
        input_text=request.text,
        predicted_label=prediction["predicted_label"],
        confidence_score=prediction["confidence_score"],
        model_version=prediction["model_version"],
    )

    logger.info(
        "Decision created",
        extra={
            "extra_data": {
                "decision_id": decision.id,
                "predicted_label": decision.predicted_label,
                "model_version": decision.model_version,
            }
        },
    )

    # Step 3: Return response to client
    return DecisionResponse(
        decision_id=decision.id,
        predicted_label=decision.predicted_label,
        confidence_score=decision.confidence_score,
        model_version=decision.model_version,
    )


# --------------------------------------------------------
# 2️⃣ ADD HUMAN REVIEW
# --------------------------------------------------------
# Where to POST:
# POST http://localhost:8000/decisions/{decision_id}/review
#
# Example:
# POST http://localhost:8000/decisions/1/review
#
# Body:
# {
#   "reviewer_name": "Anita",
#   "overridden_label": "LOW_RISK",
#   "comments": "False positive after manual check"
# }
# --------------------------------------------------------
@router.post("/decisions/{decision_id}/review")
def add_review(
    decision_id: int,
    request: ReviewRequest,
    db: Session = Depends(get_db),
):
    # Step 1: Check if decision exists
    decision = db.query(AIDecision).filter(AIDecision.id == decision_id).first()
    if decision is None:
        raise HTTPException(status_code=404, detail="Decision not found")

    # Step 2: Create review record (do NOT overwrite AI decision)
    review = DecisionReview(
        decision_id=decision_id,
        reviewer_name=request.reviewer_name,
        overridden_label=request.overridden_label,
        comments=request.comments,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    # Step 3: Log review creation
    logger.info(
        "Review added",
        extra={
            "extra_data": {
                "decision_id": review.decision_id,
                "review_id": review.id,
                "reviewer_name": review.reviewer_name,
            }
        },
    )

    # Step 4: Return confirmation response
    return {
        "review_id": review.id,
        "decision_id": review.decision_id,
        "reviewer_name": review.reviewer_name,
        "overridden_label": review.overridden_label,
        "comments": review.comments,
    }
