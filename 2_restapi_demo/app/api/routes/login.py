# Token Endpoint (Login)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas import Token
from core.security import verify_password, create_access_token
from core.config import settings
from sqlalchemy import func
from api.deps import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from datetime import datetime, timedelta
from crud import authenticate


router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token)