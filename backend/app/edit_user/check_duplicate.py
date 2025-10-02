from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Users as User
from data.postgresDB import SessionLocal
from typing import Optional
from pydantic import BaseModel

load_dotenv()  # .env 파일 자동 로드
# 유저 정보
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class UserRead(BaseModel):
    id: int
    nickname: str
    role: str
    email: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    password: Optional[str] = None
    email: str

    class Config:
        from_attributes = True

router.get("/{email}/duplicate", response_model=UserRead)
def check_duplicate_email(email:str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"message": "회원가입이 가능합니다."}
    if user.oauth is not None:
        return {"message":"회원가입이 소셜로그인으로 되어 있습니다."}
    return {"message": "이 이메일은 이미 존재합니다. 로그인 하시거나 비밀번호 재설정을 진행해주세요."}

router.get("/{nickname}/duplicate", response_model=UserRead)
def check_duplicate_nickname(nickname:str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nickname == nickname).first()
    if not user:
        return {"message": "회원가입이 가능한 닉네임입니다."}
    return {"message": "이 닉네임은 이미 존재합니다. 다른 닉네임을 사용해주세요."}

# 부모 닉네임을 따로 사용할 시
# router.get("/{parent_nickname}/duplicate", response_model=UserRead)
# def check_duplicate_parent_nickname(parent_nickname:str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.parent_nickname == parent_nickname).first()
#     if not user:
#         return {"message": "회원가입이 가능한 닉네임입니다."}
#     return {"message": "이 닉네임은 이미 존재합니다. 다른 닉네임을 사용해주세요."}