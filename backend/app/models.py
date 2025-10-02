from typing import List, Optional

from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Column, DateTime, Double, ForeignKeyConstraint, Identity, Index, Integer, PrimaryKeyConstraint, SmallInteger, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint("oauth::text = ANY (ARRAY['google'::character varying, 'naver'::character varying, 'kakao'::character varying]::text[])", name='users_oauth_check'),
        CheckConstraint("role::text = ANY (ARRAY['customer'::character varying, 'admin'::character varying]::text[])", name='users_role_check'),
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('phone', name='users_phone_key')
    )

    id = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1))
    login_id = mapped_column(String(30))
    password = mapped_column(String(255))
    name = mapped_column(String(20))
    nickname = mapped_column(String(20))
    age = mapped_column(Integer)
    gender = mapped_column(String(10))
    phone = mapped_column(String(20))
    oauth = mapped_column(String(20))
    role = mapped_column(String(20))
    email = mapped_column(String(255))
    created_at = mapped_column(DateTime, server_default=text('now()'))
    updated_at = mapped_column(DateTime, server_default=text('now()'))
    key_parent = mapped_column(String(100), server_default=text('NULL::character varying'))

    customer_support: Mapped[List['CustomerSupport']] = relationship('CustomerSupport', uselist=True, back_populates='user')
    daily_writings: Mapped[List['DailyWritings']] = relationship('DailyWritings', uselist=True, back_populates='user')
    diary: Mapped[List['Diary']] = relationship('Diary', uselist=True, back_populates='user')
    outputs: Mapped[List['Outputs']] = relationship('Outputs', uselist=True, back_populates='user')
    parent_forum_posts: Mapped[List['ParentForumPosts']] = relationship('ParentForumPosts', uselist=True, back_populates='user')
    reading_forum_posts: Mapped[List['ReadingForumPosts']] = relationship('ReadingForumPosts', uselist=True, back_populates='user')
    reading_logs: Mapped[List['ReadingLogs']] = relationship('ReadingLogs', uselist=True, back_populates='user')
    subscriptions: Mapped[List['Subscriptions']] = relationship('Subscriptions', uselist=True, back_populates='user')
    user_games: Mapped[List['UserGames']] = relationship('UserGames', uselist=True, back_populates='user')
    user_tests: Mapped[List['UserTests']] = relationship('UserTests', uselist=True, back_populates='user')


class Words(Base):
    __tablename__ = 'words'
    __table_args__ = (
        PrimaryKeyConstraint('word_id', name='words_pkey'),
        UniqueConstraint('word_text', name='words_word_text_key')
    )

    word_id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    word_text = mapped_column(Text, nullable=False)
    definition = mapped_column(Text)
    synonyms = mapped_column(ARRAY(Text()))
    embedding = mapped_column(ARRAY(Double(precision=53)))

    user_word_usage: Mapped[List['UserWordUsage']] = relationship('UserWordUsage', uselist=True, back_populates='word')

class CustomerSupport(Base):
    __tablename__ = 'customer_support'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['open'::character varying, 'in_progress'::character varying, 'resolved'::character varying, 'closed'::character varying]::text[])", name='customer_support_status_check'),
        ForeignKeyConstraint(['parent_id'], ['customer_support.id'], ondelete='CASCADE', name='customer_support_parent_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='customer_support_user_id_fkey'),
        PrimaryKeyConstraint('id', name='customer_support_pkey')
    )

    id = mapped_column(Integer)
    user_id = mapped_column(Integer)
    parent_id = mapped_column(Integer)
    category = mapped_column(String(50))
    title = mapped_column(String(255))
    content = mapped_column(Text)
    status = mapped_column(String(20))
    created_at = mapped_column(DateTime, server_default=text('now()'))
    updated_at = mapped_column(DateTime, server_default=text('now()'))

    parent: Mapped[Optional['CustomerSupport']] = relationship('CustomerSupport', remote_side=[id], back_populates='parent_reverse')
    parent_reverse: Mapped[List['CustomerSupport']] = relationship('CustomerSupport', uselist=True, remote_side=[parent_id], back_populates='parent')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='customer_support')


class DailyWritings(Base):
    __tablename__ = 'daily_writings'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='daily_writings_user_id_fkey'),
        PrimaryKeyConstraint('id', name='daily_writings_pkey')
    )

    id = mapped_column(Integer)
    created_at = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    content = mapped_column(Text, nullable=False)
    user_id = mapped_column(Integer)
    attachment_url = mapped_column(String(255))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='daily_writings')


class Diary(Base):
    __tablename__ = 'diary'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='fk_diary_user'),
        PrimaryKeyConstraint('id', name='diary_pkey')
    )

    id = mapped_column(Integer)
    created_at = mapped_column(DateTime, server_default=text('now()'))
    text_ = mapped_column('text', Text)
    user_id = mapped_column(Integer)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='diary')


class Outputs(Base):
    __tablename__ = 'outputs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='outputs_user_id_fkey'),
        PrimaryKeyConstraint('record_id', name='outputs_pkey')
    )

    record_id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    user_id = mapped_column(Integer)
    timestamp = mapped_column(DateTime(True), server_default=text('now()'))
    source = mapped_column(Text)
    content_summary = mapped_column(JSONB)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='outputs')
    user_word_usage: Mapped[List['UserWordUsage']] = relationship('UserWordUsage', uselist=True, back_populates='record')


class ParentForumPosts(Base):
    __tablename__ = 'parent_forum_posts'
    __table_args__ = (
        ForeignKeyConstraint(['parent_id'], ['parent_forum_posts.id'], ondelete='CASCADE', name='parent_forum_posts_parent_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='parent_forum_posts_user_id_fkey'),
        PrimaryKeyConstraint('id', name='parent_forum_posts_pkey')
    )

    id = mapped_column(Integer)
    content = mapped_column(Text, nullable=False)
    user_id = mapped_column(Integer)
    parent_id = mapped_column(Integer)
    title = mapped_column(String(255))
    created_at = mapped_column(DateTime, server_default=text('now()'))
    updated_at = mapped_column(DateTime, server_default=text('now()'))
    category = mapped_column(String(50))
    is_important = mapped_column(Boolean, server_default=text('false'))

    parent: Mapped[Optional['ParentForumPosts']] = relationship('ParentForumPosts', remote_side=[id], back_populates='parent_reverse')
    parent_reverse: Mapped[List['ParentForumPosts']] = relationship('ParentForumPosts', uselist=True, remote_side=[parent_id], back_populates='parent')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='parent_forum_posts')


class ReadingForumPosts(Base):
    __tablename__ = 'reading_forum_posts'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='reading_forum_posts_user_id_fkey'),
        ForeignKeyConstraint(['parent_id'], ['reading_forum_posts.id'], ondelete='CASCADE', name='reading_forum_posts_parent_id_fkey'),
        PrimaryKeyConstraint('id', name='reading_forum_posts_pkey'),
    )

    id = mapped_column(Integer)
    user_id = mapped_column(Integer, nullable=False)
    parent_id = mapped_column(Integer, nullable=True, server_default=text("NULL"))
    title = mapped_column(String(255), nullable=True)   # SQL에서 NOT NULL 제약이 없음
    content = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime, server_default=text('NOW()'))
    updated_at = mapped_column(DateTime, server_default=text('NOW()'))
    book_title = mapped_column(String(255), nullable=True)
    discussion_tags = mapped_column(String(100), nullable=True)

    # 관계 설정
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='reading_forum_posts')
    parent: Mapped[Optional['ReadingForumPosts']] = relationship(
        'ReadingForumPosts',
        remote_side=[id],
        back_populates="children"
    )
    children: Mapped[list['ReadingForumPosts']] = relationship(
        'ReadingForumPosts',
        back_populates="parent",
        cascade="all, delete-orphan"
    )


class ReadingLogs(Base):
    __tablename__ = 'reading_logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='reading_logs_user_id_fkey'),
        PrimaryKeyConstraint('id', name='reading_logs_pkey')
    )

    id = mapped_column(Integer)
    created_at = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    book_title = mapped_column(String(255), nullable=False)
    user_id = mapped_column(Integer)
    updated_at = mapped_column(DateTime)
    author = mapped_column(String(255))
    publisher = mapped_column(String(255))
    content = mapped_column(String(200))
    unknown_sentence = mapped_column(Text)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='reading_logs')


class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['active'::character varying, 'expired'::character varying, 'canceled'::character varying]::text[])", name='subscriptions_status_check'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='subscriptions_user_id_fkey'),
        PrimaryKeyConstraint('id', name='subscriptions_pkey')
    )

    id = mapped_column(Integer)
    plan_name = mapped_column(String(50), nullable=False)
    start_date = mapped_column(DateTime, nullable=False)
    end_date = mapped_column(DateTime, nullable=False)
    user_id = mapped_column(Integer)
    status = mapped_column(String(20), server_default=text("'active'::character varying"))
    created_at = mapped_column(DateTime, server_default=text('now()'))
    updated_at = mapped_column(DateTime, server_default=text('now()'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='subscriptions')


class UserGames(Base):
    __tablename__ = 'user_games'
    __table_args__ = (
        CheckConstraint("game_type::text = ANY (ARRAY['word_chain'::character varying, 'word_meaning'::character varying, 'sentence_completion'::character varying]::text[])", name='user_games_game_type_check'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_games_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_games_pkey')
    )

    id = mapped_column(Integer)
    user_id = mapped_column(Integer)
    game_type = mapped_column(String(50))
    played_at = mapped_column(DateTime, server_default=text('now()'))
    score = mapped_column(Integer)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='user_games')


class UserTests(Base):
    __tablename__ = 'user_tests'
    __table_args__ = (
        CheckConstraint("test_type::text = ANY (ARRAY['literacy'::character varying, 'vocabulary'::character varying]::text[])", name='user_tests_test_type_check'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_tests_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_tests_pkey')
    )

    id = mapped_column(Integer)
    questions = mapped_column(JSONB, nullable=False)
    user_id = mapped_column(Integer)
    test_type = mapped_column(String(50))
    taken_at = mapped_column(DateTime, server_default=text('now()'))
    user_answers = mapped_column(JSONB)
    total_score = mapped_column(Integer)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='user_tests')


class UserWordUsage(Base):
    __tablename__ = 'user_word_usage'
    __table_args__ = (
        ForeignKeyConstraint(['record_id'], ['outputs.record_id'], ondelete='CASCADE', name='user_word_usage_record_id_fkey'),
        ForeignKeyConstraint(['word_id'], ['words.word_id'], ondelete='CASCADE', name='user_word_usage_word_id_fkey'),
        PrimaryKeyConstraint('usage_id', name='user_word_usage_pkey')
    )

    usage_id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    record_id = mapped_column(Uuid)
    word_id = mapped_column(Uuid)
    frequency = mapped_column(Integer)
    user_embedding = mapped_column(ARRAY(Double(precision=53)))

    record: Mapped[Optional['Outputs']] = relationship('Outputs', back_populates='user_word_usage')
    word: Mapped[Optional['Words']] = relationship('Words', back_populates='user_word_usage')
