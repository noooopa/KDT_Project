from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import aliased,joinedload
from sqlalchemy import func
from sqlalchemy.orm import Session
from data.postgresDB import SessionLocal
from app.models import ParentForumPosts as ParentForumPost
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()  # .env 파일 자동 로드

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserNickname(BaseModel):
    nickname: str

    class Config:
        from_attributes = True

# ✅ 글 생성 요청용
class ParentForumPostCreate(BaseModel):
    user_id: int
    parent_id: Optional[int] = None
    title: str
    content: str
    category: Optional[str] = None
    is_important: Optional[bool] = False

# ✅ 글 수정 요청용
class ParentForumPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_important: Optional[bool] = None

# ✅ 글 조회 응답용 (User 정보까지 포함)
class ParentForumPostRead(BaseModel):
    id: int
    parent_id: Optional[int]
    title: str
    content: str
    category: Optional[str]
    is_important: bool
    created_at: datetime
    updated_at: datetime
    children: List["ParentForumPostRead"] = Field(default_factory=list)  # ✅ 안전한 기본값
    user: UserNickname
    comment_count: int = 0

    class Config:
        from_attributes = True

# ForwardRef 갱신
ParentForumPostRead.model_rebuild()

@router.get("/posts", response_model=list[ParentForumPostRead])
def get_posts(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(10, ge=1, le=50, description="한 페이지당 게시글 수"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size
    comment = aliased(ParentForumPost)

    subq = (
        db.query(
            ParentForumPost.id.label("post_id"),
            func.count(comment.id).label("comment_count")
        )
        .outerjoin(comment, comment.parent_id == ParentForumPost.id)
        .filter(ParentForumPost.parent_id == None)
        .group_by(ParentForumPost.id)
        .subquery()
    )

    query = (
        db.query(ParentForumPost, subq.c.comment_count)
        .join(subq, subq.c.post_id == ParentForumPost.id)
        .options(joinedload(ParentForumPost.user))  # ✅ 유저 닉네임 미리 로딩
        .order_by(ParentForumPost.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    results = query.all()

    response = []
    for post, comment_count in results:
        response.append(
            ParentForumPostRead(
                id=post.id,
                title=post.title,
                parent_id=post.parent_id,
                content=post.content,
                category=post.category,
                is_important=post.is_important,
                created_at=post.created_at,
                updated_at=post.updated_at,
                comment_count=comment_count,
                user=post.user   # ✅ UserNickname 모델로 자동 직렬화
            )
        )
    return response

@router.get("/post/{list_id}",response_model=ParentForumPostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(ParentForumPost).filter(ParentForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail={"성공여부":False,"이유":"존재하지 않는 게시물입니다."})
    return post

@router.post("/post/create", response_model=ParentForumPostCreate)
def create_post(
    request: ParentForumPostCreate,
    db: Session = Depends(get_db)
):
    new_post = ParentForumPost(
        user_id=request.user_id,
        title=request.title,
        content=request.content,
        category=request.category,
        is_important=request.is_important,
        parent_id=request.parent_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.patch("/post/{list_id}/update",response_model=ParentForumPostUpdate)
def update_post(
    request: ParentForumPostUpdate,
    list_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(ParentForumPost).filter(ParentForumPost.id == list_id).first()
    if not post:
        raise HTTPException(status_code=404, detail={"성공여부":False,"이유":"존재하지 않는 게시물입니다."})
    if request.title:
        post.title = request.title
        post.updated_at = datetime.now()
        post.content = request.content
        db.commit()
        db.refresh(post)
        return post
    return {"로그":"수정될 것이 없거나 실패했습니다."}
@router.delete("/post/{list_id}/delete")
def delete_post(
    list_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(ParentForumPost).filter(ParentForumPost.id == list_id).first()
    if not post:
        raise HTTPException(status_code=404, detail={"성공여부":False,"이유":"존재하지 않는 게시물입니다."})
    db.delete(post)
    db.commit()
    return {"성공여부": True}