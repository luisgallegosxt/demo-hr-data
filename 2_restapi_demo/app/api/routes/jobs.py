from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Job as JobModels
from schemas import JobCreate, Job
from api.deps import get_current_user
from sqlalchemy import func
from api.deps import get_db
from logger import app_logger

router = APIRouter()

@router.post("/", response_model=List[Job])
def create_jobs(jobs: List[JobCreate], db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if len(jobs) > 1000:
        app_logger.warning("Cannot insert more than 1000 records at a time", exc_info=True)
        raise HTTPException(status_code=400, detail="Cannot insert more than 1000 records at a time")

    max_id = db.query(func.max(JobModels.id)).scalar() or 0
    new_jobs = [JobModels(id=max_id + i + 1, **job.dict()) for i, job in enumerate(jobs)]
    db.bulk_save_objects(new_jobs)
    db.commit()
    return new_jobs
