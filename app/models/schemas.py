from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class EmergencyRequestCreate(BaseModel):
    name: str
    location: str
    description: str
    contact_number: str
    language: str = "English"

class EmergencyRequestResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str
    contact_number: str
    language: str
    category: str
    urgency: str
    required_resources: str
    summary: str
    hindi_summary: str
    recommendations: str
    timestamp: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_requests: int
    critical_count: int
    category_counts: dict
    recent_requests: List[EmergencyRequestResponse]
