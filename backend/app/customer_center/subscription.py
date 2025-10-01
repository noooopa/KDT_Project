from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from data.postgresDB import SessionLocal
from app.models import Users
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()  # .env 파일 자동 로드

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 토스 결제 승인 API (테스트 환경도 동일 URL)
TOSS_URL = "https://api.tosspayments.com/v1/payments/confirm"



