from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from data.postgresDB import SessionLocal
from app.models import User
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


class AdditionalInfo(BaseModel):
    user_id: int
    nickname: str
    age: int
    gender: str
    phone: str
    role: str

    class Config:
        from_attribute = True  # ORM → Pydantic 변환 허용
@router.get("/additional-info")
async def additional_info_form(user_id: int):
    # React 추가정보 입력 페이지로 바로 리다이렉트
    return RedirectResponse(url=f"http://localhost:5173/additional-info?user_id={user_id}")

@router.patch("/additional-info/{user_id}")
async def additional_info(
        user_id: int,
        data: AdditionalInfo=Body(...),
        db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    user.nickname = data.nickname
    user.age = data.age
    user.gender = data.gender
    user.phone = data.phone
    user.role = data.role
    db.commit()
    db.refresh(user)

    return {"message": "User info updated", "user_id": user.id}
