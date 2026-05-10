from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .database import database, models
from .models import schemas
from .ai import workflow
from .services import ngo_service

app = FastAPI(title="ReliefLink AI API")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

@app.post("/requests/", response_model=schemas.EmergencyRequestResponse)
async def create_request(request: schemas.EmergencyRequestCreate, db: Session = Depends(database.get_db)):
    # Run AI Workflow
    ngo_data = ngo_service.get_ngo_dataset_str()
    ai_results = await workflow.run_ai_workflow(request.description, request.location, ngo_data)
    
    db_request = models.EmergencyRequest(
        **request.dict(),
        category=ai_results["category"],
        urgency=ai_results["urgency"],
        required_resources=ai_results["required_resources"],
        summary=ai_results["summary"],
        hindi_summary=ai_results["hindi_summary"],
        recommendations=ai_results["recommendations"]
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@app.get("/requests/", response_model=List[schemas.EmergencyRequestResponse])
def read_requests(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    requests = db.query(models.EmergencyRequest).offset(skip).limit(limit).all()
    return requests

@app.get("/stats/", response_model=schemas.DashboardStats)
def get_stats(db: Session = Depends(database.get_db)):
    total = db.query(models.EmergencyRequest).count()
    critical = db.query(models.EmergencyRequest).filter(models.EmergencyRequest.urgency == "CRITICAL").count()
    
    # Category counts
    category_counts = {}
    all_requests = db.query(models.EmergencyRequest).all()
    for req in all_requests:
        category_counts[req.category] = category_counts.get(req.category, 0) + 1
        
    recent = db.query(models.EmergencyRequest).order_by(models.EmergencyRequest.timestamp.desc()).limit(5).all()
    
    return {
        "total_requests": total,
        "critical_count": critical,
        "category_counts": category_counts,
        "recent_requests": recent
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
