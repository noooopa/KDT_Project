from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from fastapi.requests import Request
from app.customer_center.customer_support import router as customer_support
from app.edit_user.edit_user import router as edit_user
from app.forum.parent import router as parent
from app.login.register import router as register
from app.login.naver_router import router as naver_router
from app.login.google import router as google_router
from app.login.additional_info import router as additional_info_router
from app.login.kakao_router import router as kakao_router
from app.login.login import router as login
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()
app = FastAPI()
SECRET_KEY = os.getenv("SECRET_KEY")

# ✅ CORS 설정
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",   # React 개발 환경
    "http://127.0.0.1:5173",
    "https://your-frontend-domain.com"  ]
#배포환경

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 허용할 도메인
    allow_credentials=True,           # 쿠키 인증을 허용할지
    allow_methods=["*"],              # 허용할 HTTP 메소드
    allow_headers=["*"],              # 허용할 HTTP 헤더
)
# --- SessionMiddleware 추가 --- # 반드시 안전한 키로 교체
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
# OAuth 라우트 등록
app.include_router(additional_info_router, prefix="/auth", tags=["auth"])
app.include_router(google_router, prefix="/auth/google", tags=["google"])
app.include_router(naver_router, prefix="/auth/naver", tags=["naver"])
app.include_router(kakao_router, prefix="/auth/kakao", tags=["kakao"])
# 고객센터
app.include_router(customer_support, prefix="/customer-support", tags=["customer-support"])
# 사용자 정보 수정/삭제
app.include_router(edit_user, prefix="/user", tags=["user"])
# 로그인/상태관리
app.include_router(login, prefix="/login_user", tags=["login"])
# 회원가입
app.include_router(register, prefix="/register", tags=["register"])
#커뮤니티
app.include_router(parent,prefix="/community/parent",tags=["community_parent"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
