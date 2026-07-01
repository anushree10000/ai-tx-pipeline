import uuid
from sqlalchemy import Column, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"))
    txn_id = Column(String, nullable=True)  # Can be blank in dirty data
    date = Column(String, nullable=True)    # Normalized ISO 8601 string (YYYY-MM-DD)
    merchant = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=True)
    status = Column(String, nullable=True)
    category = Column(String, nullable=True)
    account_id = Column(String, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    anomaly_reason = Column(Text, default="")

    job = relationship("Job", back_populates="transactions")