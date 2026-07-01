from pydantic import BaseModel
from typing import Optional, List
from src.schemas.job import JobSummarySchema

class TransactionSchema(BaseModel):
    txn_id: Optional[str] = None
    date: Optional[str] = None
    merchant: Optional[str] = None
    amount: float
    currency: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    account_id: Optional[str] = None
    is_anomaly: bool
    anomaly_reason: str

    class Config:
        from_attributes = True

class JobFullResultsResponse(BaseModel):
    job_id: str
    status: str
    cleaned_transactions: List[TransactionSchema]
    flagged_anomalies: List[TransactionSchema]
    per_category_breakdown: Dict[str, float]  # e.g., {"Food": 1500.0}
    summary: Optional[JobSummarySchema] = None