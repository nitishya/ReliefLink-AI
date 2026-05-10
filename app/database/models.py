from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base

class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    description = Column(Text)
    contact_number = Column(String)
    language = Column(String, default="English")
    
    # AI Processed Fields
    category = Column(String)
    urgency = Column(String) # LOW, MEDIUM, HIGH, CRITICAL
    required_resources = Column(Text)
    summary = Column(Text)
    hindi_summary = Column(Text)
    recommendations = Column(Text) # JSON string of NGO contacts
    
    timestamp = Column(DateTime, default=datetime.utcnow)
