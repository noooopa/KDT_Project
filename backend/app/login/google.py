# google.py
import httpx
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
import os
from app.models import User
from data.postgresDB import SessionLocal
from jose import jwt
from dotenv import load_dotenv
load_dotenv()  # .env 파일 자동 로드
router = APIRouter()   # ✅ 모듈별 라우터

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

@router.get("/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)

    id_token = token.get("id_token")
    user_info = None

    if id_token:
        # 검증 없이 claims 추출 (테스트용)
        user_info = jwt.get_unverified_claims(id_token)
    else:
        # fallback: access_token으로 userinfo API 호출
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token['access_token']}"}
            )
            user_info = resp.json()

        return {"user": user_info}

    # DB 저장 로직
    user = db.query(User).filter(User.email == user_info["email"]).first()
    if not user:
        user = User(email=user_info["email"], name=user_info.get("name"), oauth="google")
        db.add(user)
        db.commit()
        db.refresh(user)
        return RedirectResponse(f"http://localhost:5173/additional-info?userId={user.id}")

    return RedirectResponse("http://localhost:5173/profile")
