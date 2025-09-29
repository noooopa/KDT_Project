from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
import os
from app.models import User
from data.postgresDB import SessionLocal
from dotenv import load_dotenv
load_dotenv()  # .env 파일 자동 로드

router = APIRouter()
oauth = OAuth()

oauth.register(
    name="naver",
    client_id=os.getenv("NAVER_CLIENT_ID"),
    client_secret=os.getenv("NAVER_CLIENT_SECRET"),
    authorize_url="https://nid.naver.com/oauth2.0/authorize",
    access_token_url="https://nid.naver.com/oauth2.0/token",
    api_base_url="https://openapi.naver.com/v1/nid/",
    client_kwargs={"scope": "name email"},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login")
async def naver_login(request: Request):
    redirect_uri = request.url_for("naver_callback")
    return await oauth.naver.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def naver_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.naver.authorize_access_token(request)
    except Exception as e:
        return {"error": f"Token exchange failed: {str(e)}"}

    try:
        resp = await oauth.naver.get("me", token=token)   # ✅ userinfo → me
        user_info = resp.json().get("response")
    except Exception as e:
        return {"error": f"Userinfo request failed: {str(e)}"}

    if not user_info:
        return {"error": "Naver authentication failed"}

    email = user_info.get("email")
    if not email:
        return {"error": "Naver did not return email. Check consent settings."}

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, name=user_info.get("name"), oauth="naver")
        db.add(user)
        db.commit()
        db.refresh(user)
        return RedirectResponse(f"http://localhost:5173/additional-info?userId={user.id}")

    return RedirectResponse("http://localhost:5173/profile")

