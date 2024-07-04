from fastapi import APIRouter, HTTPException
from api.routes import departments, jobs, hired_employees, login

api_router = APIRouter()

api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(hired_employees.router, prefix="/hired_employees", tags=["hired_employees"])
api_router.include_router(login.router, tags=["login"])

