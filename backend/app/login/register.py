import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Users as User
from data.postgresDB import SessionLocal
from app.edit_user.edit_user import UserRead

load_dotenv()  # .env 파일 자동 로드
router = APIRouter()   # ✅ 모듈별 라우터

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
SECRET_KEY=os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

class UserRegister(BaseModel):
    login_id: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    oauth: Optional[str] = None
    email: str
    name: str

    class Config:
        from_attributes = True

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/new", response_model=UserRead)
def register(data: UserRegister, db: Session = Depends(get_db)):
    # 이메일 중복 검사
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ 비밀번호 해시
    hashed_pw = hash_password(data.password)

    user = User(
        login_id=data.login_id,
        email=data.email,
        name=data.name,
        password=hashed_pw,   # 해시된 비밀번호 저장
        nickname=data.nickname,
        phone=data.phone,
        gender=data.gender,
        age=data.age,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user