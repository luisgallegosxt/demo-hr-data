from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.security import verify_password, get_password_hash
from models import User, Department, Job, HiredEmployee
from schemas import UserCreate, HiredEmployeeCreate
from typing import List
from sqlalchemy import func
from datetime import datetime
from logger import app_logger

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    max_id = db.query(func.max(User.id)).scalar() or 0
    db_user = User(id=max_id + 1, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        app_logger.warning("Incorrect username or password", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    return user


def get_department(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id).first()


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def create_hired_employees(db: Session, hired_employees: List[HiredEmployeeCreate]):
    if len(hired_employees) > 1000:
        app_logger.warning("Cannot insert more than 1000 records at a time", exc_info=True)
        raise HTTPException(status_code=400, detail="Cannot insert more than 1000 records at a time")
    
    for emp in hired_employees:
        if not get_department(db, emp.department_id):
            app_logger.warning(f"Department ID {emp.department_id} does not exist", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Department ID {emp.department_id} does not exist")
        if not get_job(db, emp.job_id):
            app_logger.warning(f"Job ID {emp.job_id} does not exist", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Job ID {emp.job_id} does not exist")

    max_id = db.query(func.max(HiredEmployee.id)).scalar() or 0
    # new_hired_employees = [HiredEmployee(id=max_id + i + 1, datetime=datetime.now(), **emp.dict()) for i, emp in enumerate(hired_employees)]
    new_hired_employees = []
    for i, emp in enumerate(hired_employees):
        emp_data = emp.dict()
        emp_data["id"] = max_id + i + 1
        emp_data["datetime"] = datetime.now()
        new_hired_employee = HiredEmployee(**emp_data)
        new_hired_employees.append(new_hired_employee)
    
    db.bulk_save_objects(new_hired_employees)
    db.commit()
    return new_hired_employees