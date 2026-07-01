from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class JobSummarySchema(BaseModel):
    total_spend_usd: float
    total_spend_inr: float
    top_merchants: List[str]
    anomaly_count: int
    narrative: str
    risk_level: str

    class Config:
        from_attributes = True

class JobStatusResponse(BaseModel):
    id: str
    filename: str
    status: str
    row_count_raw: Optional[int] = None
    row_count_clean: Optional[int] = None
    created_at: datetime
    summary: Optional[JobSummarySchema] = None

    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    id: str
    filename: str
    status: str
    row_count_raw: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True