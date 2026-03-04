# AI Decision Audit & Logging System
## Overview

This project is a production-style backend system built using FastAPI and MySQL that simulates an AI risk classification engine with full audit traceability.

The system demonstrates how AI decisions can be logged, reviewed, and governed using a human-in-the-loop design.

The focus is on backend architecture, audit compliance, structured logging, and clean separation of concerns.

## Key Features

AI-based risk prediction endpoint

* Confidence scoring with model version tracking

* MySQL persistence of all decisions

* Separate human review table (no overwrite of AI output)

* Structured JSON logging

* Proper service-layer architecture

* Basic error handling (404 for missing decisions)

* Clean, scalable folder structure

## Tech Stack

* FastAPI

* SQLAlchemy

* MySQL

* Pydantic

* Structured Logging (JSON format)

* Python 3.11

## Architecture Design

The system follows a layered backend structure:

Configuration Layer → environment and database setup
Database Layer → SQLAlchemy models
Service Layer → business logic abstraction
API Layer → request handling

This ensures modularity, scalability, and maintainability.

Database Schema
Table: ai_decisions

id

input_text

predicted_label

confidence_score

model_version

created_at

Table: decision_reviews

id

decision_id (Foreign Key)

reviewer_name

overridden_label

comments

reviewed_at

AI decisions are never overwritten.
Human reviews are stored separately to preserve audit history.

API Endpoints
Create Decision

POST /decision

Request:
{
"text": "Suspicious transaction detected"
}

Response:
{
"decision_id": 1,
"predicted_label": "HIGH_RISK",
"confidence_score": 0.9,
"model_version": "v3.0"
}

Review Decision

POST /decision/{decision_id}/review

Request:
{
"decision_id": 1,
"reviewer_name": "Anita",
"overridden_label": "MEDIUM_RISK",
"comments": "Manual verification completed"
}

Returns 404 if decision does not exist.

How To Run Locally

Create virtual environment

Activate environment

Install dependencies
pip install -r requirements.txt

Create MySQL database
CREATE DATABASE ai_audit_db;

Run server
uvicorn app.main:app --reload

Open
http://127.0.0.1:8000/docs

Future Improvements

Replace rule engine with trained ML model

Add authentication & role-based access

Integrate Alembic for schema migrations

Add monitoring & metrics

Containerize with Docker

Author

Backend-focused AI governance project demonstrating production-ready architecture principles.
