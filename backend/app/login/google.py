# google.py
import httpx
from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
import os,datetime
from app.models import User
from data.postgresDB import SessionLocal
from jose import jwt
from dotenv import load_dotenv
from typing import Any, Optional
load_dotenv()  # .env 파일 자동 로드
router = APIRouter()   # ✅ 모듈별 라우터
ALGORITHM = "HS256"

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
# OAuth 설정
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
SECRET_KEY=os.environ.get("SECRET_KEY")

def create_token(user_id: int):
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)

    id_token = token.get("id_token")
    user_info: Optional[dict[str, Any]] = None

    if id_token:
        user_info = jwt.get_unverified_claims(id_token)
    else:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token['access_token']}"}
            )
            user_info = resp.json()

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

        # ✅ DB 조회
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        # 신규 회원이면 추가정보 입력 페이지로
        user = User(email=user_info["email"], name=user_info.get("name"), oauth="google")
        db.add(user)
        db.commit()
        db.refresh(user)
        return RedirectResponse(f"http://localhost:5173/additional-info?email={user.email}")

    # ✅ JWT 발급
    access_token = create_token(user.id)

    # ✅ 리다이렉트 응답 + httpOnly 쿠키 심기
    response = RedirectResponse("http://localhost:5173/")
    # response = RedirectResponse("/")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,   # 자바스크립트 접근 불가, XSS 방지
        secure=False,     # HTTPS에서만 전송 (개발 중이면 False 가능), 현재 개발중
        samesite="lax",  # 크로스사이트 요청 제한
        max_age=3600,    # 1시간 (exp와 맞추기)
    )
    return response
