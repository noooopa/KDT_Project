from app.models import Users as User
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Cookie, Depends, HTTPException, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
from jose import jwt, JWTError

from data.postgresDB import SessionLocal

load_dotenv()  # .env 파일 자동 로드
router = APIRouter()   # ✅ 모듈별 라우터

class LoginSchema(BaseModel):
    email:str
    password: str

def create_access_token(user_id: int, expires_delta: int = 60):
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int, expires_days: int = 7):
    expire = datetime.utcnow() + timedelta(days=expires_days)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
SECRET_KEY=os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/profile-data")
def profile_data(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "name": user.name, "nickname": user.nickname, "role":user.role}
# 로그인 상태 유지
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    # ✅ 소셜 로그인 유저는 비밀번호 없음
    if user.oauth:
        raise HTTPException(status_code=400, detail=f"소셜 {user.oauth} 로그인을 사용하세요")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="이메일이나 비밀번호가 틀렸습니다.")

    # JWT 발급
    access_token = create_access_token(user.id, expires_delta=15)   # 15분짜리
    refresh_token = create_refresh_token(user.id, expires_days=7)  # 7일짜리
    response = JSONResponse({"msg": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,   # 개발용
        samesite="lax",
        max_age=3600,
    )
    return response

@router.post("/refresh")
def refresh_token(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token expired")

    # DB에서 유저 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 새 access token 발급
    new_access_token = create_access_token(user.id, expires_delta=15)
    response = JSONResponse({"msg": "Token refreshed"})
    response.set_cookie("access_token", new_access_token, httponly=True, max_age=900)
    return response
@router.get("/logout")
def logout():
    response = RedirectResponse("http://localhost:5173/")
    response.delete_cookie("access_token")
    return response