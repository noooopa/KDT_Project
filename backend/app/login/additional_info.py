from fastapi import APIRouter, Depends, Body
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from data.postgresDB import SessionLocal
from app.models import Users as User
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
    email: str

    class Config:
        from_attribute = True  # ORM → Pydantic 변환 허용
@router.get("/additional-info")
async def additional_info_form(email: str):
    # React 추가정보 입력 페이지로 바로 리다이렉트
    return RedirectResponse(url=f"http://localhost:5173/additional-info?email={email}")

@router.patch("/additional-info/{email}")
async def additional_info(
        email: str,
        data: AdditionalInfo=Body(...),
        db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"error": "User not found"}

    user.nickname = data.nickname
    user.age = data.age
    user.gender = data.gender
    user.phone = data.phone
    user.role = data.role
    db.commit()
    db.refresh(user)

    return {"message": "User info updated", "email": user.email}
