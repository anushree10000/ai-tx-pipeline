import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from src.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    row_count_raw = Column(Integer, nullable=True)
    row_count_clean = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    transactions = relationship("Transaction", back_populates="job", cascade="all, delete-orphan")
    summary = relationship("JobSummary", back_populates="job", uselist=False, cascade="all, delete-orphan")


class JobSummary(Base):
    __tablename__ = "job_summaries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"), unique=True)
    total_spend_usd = Column(Float, default=0.0)
    total_spend_inr = Column(Float, default=0.0)
    top_merchants = Column(JSON, default=list)  # Stored as a list of strings
    anomaly_count = Column(Integer, default=0)
    narrative = Column(Text, nullable=True)
    risk_level = Column(String, default="low")   # low, medium, high

    job = relationship("Job", back_populates="summary")