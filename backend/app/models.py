from sqlalchemy import Column, Integer, String, DateTime, func, CheckConstraint, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from data.postgresDB import Base
# 유저 베이스 모델
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login_id=Column(String(30), nullable=True)
    password = Column(String(255), nullable=True)  # OAuth 가입자는 비밀번호 없을 수 있음
    name = Column(String(20), nullable=True)
    nickname = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    oauth = Column(String(20), CheckConstraint("oauth IN ('google','naver','kakao')"),nullable=True)
    role = Column(String(20), CheckConstraint("role IN ('customer','admin')"), default="customer")
    email = Column(String(255), unique=True, index=True, nullable=False)
    key_parent = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
# 고객센터 베이스 모델
class CustomerSupport(Base):
    __tablename__ = "customer_support"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("customer_support.id", ondelete="CASCADE"), nullable=True)  # null이면 질문, 값이 있으면 답변/댓글
    category = Column(String(50), nullable=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    status = Column(
        String(20),
        CheckConstraint("status IN ('open','in_progress','resolved','closed')"),
        default="open",
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
# 부모님 포럼 게시물 베이스모델
class ParentForumPost(Base):
    __tablename__ = "parent_forum_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    parent_id = Column(Integer, ForeignKey("parent_forum_posts.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)  # 원글일 경우 사용
    is_important = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # User와 관계
    user = relationship("User", backref="parent_forum_posts")

    # 자기참조 관계
    parent = relationship("ParentForumPost", remote_side=[id], backref="children")

