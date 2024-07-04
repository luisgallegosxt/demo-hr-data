from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Union

class DepartmentBase(BaseModel):
    department: str = Field(max_length=50)

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    job: str = Field(max_length=50)

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True

class HiredEmployeeBase(BaseModel):
    name: str = Field(max_length=50)
    department_id: int
    job_id: int

class HiredEmployeeCreate(HiredEmployeeBase):
    datetime: Union[datetime, None] = None

class HiredEmployee(HiredEmployeeBase):
    id: int
    datetime: datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"