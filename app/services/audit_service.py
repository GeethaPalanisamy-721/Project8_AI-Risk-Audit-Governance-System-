from sqlalchemy.orm import Session
from app.models.decision import AIDecision, DecisionReview


# --------------------------------------------------------
# 1️⃣ CREATE AI DECISION
# --------------------------------------------------------
def create_decision(
    db: Session,
    input_text: str,
    predicted_label: str,
    confidence_score: float,
    model_version: str,
):
    decision = AIDecision(
        input_text=input_text,
        predicted_label=predicted_label,
        confidence_score=confidence_score,
        model_version=model_version,
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision


# --------------------------------------------------------
# 2️⃣ CREATE HUMAN REVIEW
# --------------------------------------------------------
def create_review(
    db: Session,
    decision_id: int,
    reviewer_name: str,
    overridden_label: str,
    comments: str | None,
):
    # Step 1: Check if decision exists
    decision = db.query(AIDecision).filter(AIDecision.id == decision_id).first()

    if not decision:
        raise ValueError("Decision not found")

    # Step 2: Create review object
    review = DecisionReview(
        decision_id=decision_id,
        reviewer_name=reviewer_name,
        overridden_label=overridden_label,
        comments=comments,
    )

    # Step 3: Save to database
    db.add(review)
    db.commit()
    db.refresh(review)

    return review