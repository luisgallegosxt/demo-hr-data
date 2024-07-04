from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import HiredEmployeeCreate, HiredEmployee
from api.deps import get_current_user
from sqlalchemy import func
from api.deps import get_db
from crud import create_hired_employees

router = APIRouter()

@router.post("/", response_model=List[HiredEmployee])
def create_hired_employees_endpoint(hired_employees: List[HiredEmployeeCreate], db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_hired_employees(db, hired_employees)
