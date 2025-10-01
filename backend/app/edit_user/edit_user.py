from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from app.models import User
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
    login_id: Optional[str]
    name: Optional[str]
    nickname: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    phone: Optional[str] = None
    oauth: Optional[str] = None
    role: str
    email: str
    key_parent: Optional[str]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    login_id: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    key_parent: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/info/{email}", response_model=UserRead)
def info(   email: str,
            db: Session = Depends(get_db)
    ):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"error": "User not found"}
    return user

@router.patch("/info/{email}", response_model=UserRead)
def patch_info(
        email: str,
        data: UserUpdate = Body(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user
@router.delete("/info/{email}", response_model=UserRead)
def delete_info(
    email: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:db.query(User).filter(User.email == email).delete()
    except Exception as error:
        raise HTTPException(status_code=404, detail=error)
    db.commit()
    print({"message": "User deleted"})
    return RedirectResponse("http://localhost:5173/")
    # return RedirectResponse("/")
    # 서버 구동시에는 밑에껄 주석풀고 위에껄 주석해서 홈으로
