from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
import os
from app.login.google import create_token
from app.models import User
from data.postgresDB import SessionLocal

router = APIRouter()
oauth = OAuth()

oauth.register(
    name="kakao",
    client_id=os.getenv("KAKAO_CLIENT_ID"),   # ✅ REST API 키
    authorize_url="https://kauth.kakao.com/oauth/authorize",
    access_token_url="https://kauth.kakao.com/oauth/token",
    api_base_url="https://kapi.kakao.com/v2/",
    # scope 빼고 기본만 요청
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login")
async def kakao_login(request: Request):
    redirect_uri = request.url_for("kakao_callback")
    return await oauth.kakao.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="kakao_callback")
async def kakao_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.kakao.authorize_access_token(request)
    except Exception as e:
        return {"error": f"Token exchange failed: {str(e)}"}

    # ✅ 사용자 정보 요청
    try:
        resp = await oauth.kakao.get("user/me", token=token)
        user_info = resp.json()
    except Exception as e:
        return {"error": f"Userinfo request failed: {str(e)}"}

    if not user_info or "id" not in user_info:
        return {"error": "Kakao authentication failed"}

    kakao_id = user_info.get("id")

    # ✅ 이메일/닉네임이 없으므로 카카오 id를 기반으로 유저 검색
    user = db.query(User).filter(
        User.oauth == "kakao", User.name == f"kakao_{kakao_id}"
    ).first()

    if not user:
        # 신규 회원 → 임시 이메일/닉네임 생성
        user = User(
            email=f"{kakao_id}@kakao.local",   # 임시 이메일
            name=f"kakao_{kakao_id}",          # 임시 닉네임
            oauth="kakao"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return RedirectResponse(
            f"http://localhost:5173/additional-info?email={user.email}"
        )

    # ✅ JWT 발급
    access_token = create_token(user.id)

    # ✅ httpOnly 쿠키 심기
    response = RedirectResponse("http://localhost:5173/")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,   # JS 접근 불가
        secure=False,    # 개발환경 → False, 운영환경 → True
        samesite="lax",
        max_age=3600,
    )
    return response

