from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Department as DepartmentModel
from schemas import DepartmentCreate, Department
from api.deps import get_current_user
from sqlalchemy import func
from api.deps import get_db
from logger import app_logger

router = APIRouter()

@router.post("/", response_model=List[Department])
def create_departments(departments: List[DepartmentCreate], db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if len(departments) > 1000:
        app_logger.warning("Cannot insert more than 1000 records at a time", exc_info=True)
        raise HTTPException(status_code=400, detail="Cannot insert more than 1000 records at a time")
    
    max_id = db.query(func.max(DepartmentModel.id)).scalar() or 0
    new_departments = [DepartmentModel(id=max_id + i + 1, **dept.dict()) for i, dept in enumerate(departments)]
    db.bulk_save_objects(new_departments)
    db.commit()
    return new_departments