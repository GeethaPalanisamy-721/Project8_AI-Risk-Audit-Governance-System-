from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class AIDecision(Base):
    __tablename__ = "ai_decisions"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    predicted_label = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship("DecisionReview", back_populates="decision")


class DecisionReview(Base):
    __tablename__ = "decision_reviews"

    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(Integer, ForeignKey("ai_decisions.id"), nullable=False)
    reviewer_name = Column(String(100), nullable=False)
    overridden_label = Column(String(100), nullable=True)
    comments = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())

    decision = relationship("AIDecision", back_populates="reviews")