from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import aliased,joinedload
from sqlalchemy import func
from sqlalchemy.orm import Session
from data.postgresDB import SessionLocal
from app.models import ReadingForumPosts
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

# ✅ 사용자 닉네임용 (기존과 동일)
class UserNickname(BaseModel):
    nickname: str

    class Config:
        from_attributes = True


# ✅ 글 생성 요청용
class ReadingForumPostCreate(BaseModel):
    user_id: int
    parent_id: Optional[int] = None  # 부모글 ID
    title: Optional[str] = None
    content: str
    book_title: Optional[str] = None       # ✅ ORM의 book_title 반영
    discussion_tags: Optional[str] = None  # ✅ ORM의 discussion_tags 반영


# ✅ 글 수정 요청용
class ReadingForumPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    book_title: Optional[str] = None
    discussion_tags: Optional[str] = None


# ✅ 글 조회 응답용 (User 정보 + children 포함)
class ReadingForumPostRead(BaseModel):
    id: int
    parent_id: Optional[int] = None
    title: Optional[str]
    content: str
    book_title: Optional[str]
    discussion_tags: Optional[str]
    created_at: datetime
    updated_at: datetime
    children: List["ReadingForumPostRead"] = Field(default_factory=list)  # ✅ 자기참조 구조
    user: UserNickname
    comment_count: int = 0  # 댓글 개수 (추가 필드)

    class Config:
        from_attributes = True

# ForwardRef 갱신
ReadingForumPostRead.model_rebuild()

@router.get("/posts", response_model=list[ReadingForumPostRead])
def get_posts(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(10, ge=1, le=50, description="한 페이지당 게시글 수"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * size
    comment = aliased(ReadingForumPosts)

    subq = (
        db.query(
            ReadingForumPosts.id.label("post_id"),
            func.count(comment.id).label("comment_count")
        )
        .outerjoin(comment, comment.parent_id == ReadingForumPosts.id)
        .filter(ReadingForumPosts.parent_id == None)
        .group_by(ReadingForumPosts.id)
        .subquery()
    )

    query = (
        db.query(ReadingForumPosts, subq.c.comment_count)
        .join(subq, subq.c.post_id == ReadingForumPosts.id)
        .options(joinedload(ReadingForumPosts.user))  # ✅ 유저 닉네임 미리 로딩
        .order_by(ReadingForumPosts.created_at.desc())
        .offset(offset)
        .limit(size)
    )

    results = query.all()

    response = []
    for post, comment_count in results:
        response.append(
            ReadingForumPostRead(
                id=post.id,
                title=post.title,
                parent_id=post.parent_id,
                content=post.content,
                book_title=post.book_title,
                discussion_tags=post.discussion_tags,
                created_at=post.created_at,
                updated_at=post.updated_at,
                comment_count=comment_count,
                user=post.user   # ✅ UserNickname 모델로 자동 직렬화
            )
        )
    return response

@router.get("/post/{list_id}",response_model=ReadingForumPostRead)
def get_post(list_id: int, db: Session = Depends(get_db)):
    post = db.query(ReadingForumPosts).filter(ReadingForumPosts.id == list_id).first()
    if not post:
        raise HTTPException(status_code=404, detail={"성공여부":False,"이유":"존재하지 않는 게시물입니다."})
    return post

@router.post("/post/create", response_model=ReadingForumPostCreate)
def create_post(
    request: ReadingForumPostCreate,
    db: Session = Depends(get_db)
):
    new_post = ReadingForumPosts(
        user_id=request.user_id,
        title=request.title,
        content=request.content,
        book_title=request.book_title,
        discussion_tags=request.discussion_tags,
        parent_id=request.parent_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.patch("/post/{list_id}/update",response_model=ReadingForumPostUpdate)
def update_post(
    request: ReadingForumPostUpdate,
    list_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(ReadingForumPosts).filter(ReadingForumPosts.id == list_id).first()
    if not post:
        raise HTTPException(status_code=404, detail={"성공여부":False,"이유":"존재하지 않는 게시물입니다."})
    if request.title:
        post.book_title = request.book_title
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
    post = db.query(ReadingForumPosts).filter(ReadingForumPosts.id == list_id).first()
    if not post:
        raise HTTPException(status_code=404, detail={"성공여부":False,"이유":"존재하지 않는 게시물입니다."})
    db.delete(post)
    db.commit()
    return {"성공여부": True}