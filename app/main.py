from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import decision

# IMPORTANT: Import models so SQLAlchemy registers them
from app.models.decision import AIDecision, DecisionReview

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(decision.router)


@app.get("/")
def read_root():
    return {"message": "AI Decision Audit System Running"}