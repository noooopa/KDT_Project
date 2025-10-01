from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from data.postgresDB import SessionLocal
from app.models import CustomerSupport
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

class CustomerSupportCreate(BaseModel):
    user_id: int
    parent_id: Optional[int] = None  # null이면 질문, 값이 있으면 답변/댓글
    category: Optional[str] = None
    title: Optional[str] = None
    content: str
    status: Optional[str] = "open"

class CustomerSupportResponse(BaseModel):
    id: int
    user_id: int
    parent_id: Optional[int]
    category: Optional[str]
    title: Optional[str]
    content: str
    status: str

    class Config:
        from_attribute = True  # SQLAlchemy 객체를 자동 변환

@router.get("/")
async def customer_support():
    return RedirectResponse(url="/customer-support/list")
# 자주하는 질문 리스트로 넘어가도록
@router.get("/list")
async def customer_support_list(db: Session = Depends(get_db)):
    customer_support_lists = db.query(CustomerSupport).filter(CustomerSupport.parent_id == None).all()
    return customer_support_lists

@router.get("/list/{list_id}")
async def customer_support_by_id(list_id: int, db: Session = Depends(get_db)):
    try:
        post = db.query(CustomerSupport).filter(CustomerSupport.id == list_id).first()
        if not post:
            return {"message": "존재하지 않는 게시물입니다."}
        return post
    except Exception as e:
        return {"error": f"Error: {e}"}

@router.post("/list",response_model=CustomerSupportResponse)
async def customer_support_create(request: CustomerSupportCreate, db: Session = Depends(get_db)):
    # 1. parent_id가 있으면 부모 글이 존재하는지 체크
    if request.parent_id:
        parent = db.query(CustomerSupport).filter(CustomerSupport.id == request.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent post not found")
    # 2. 객체 생성
    new_post = CustomerSupport(
        user_id=request.user_id,
        parent_id=request.parent_id,
        category=request.category,
        title=request.title,
        content=request.content,
        status=request.status,
    )
    # 3. DB 저장
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
@router.patch("/list/{list_id}",response_model=CustomerSupportResponse)
async def customer_support_update(request: CustomerSupportCreate, db: Session = Depends(get_db)):
    list_id=request.parent_id
    if request.parent_id:
        parent = db.query(CustomerSupport).filter(CustomerSupport.id == list_id).first()
        parent.status="resolved"
    else:
        parent = db.query(CustomerSupport).first()
        parent.status="open"
    return parent

@router.delete("/list/{list_id}")
async def customer_support_delete(list_id: int, db: Session = Depends(get_db)):
    try: db.query(CustomerSupport).filter(
        CustomerSupport.id == list_id
    ).delete()
    except Exception as e:
        return {"error": f"Error: {e}"}
    db.commit()
    return {"success": True}

