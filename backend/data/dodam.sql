-- users
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, --다른 DB와의 호환성 고려
    login_id VARCHAR(30),
    password VARCHAR(255),
    name VARCHAR(20),
    nickname VARCHAR(20),
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(20) unique, -- String 형식이 안전, 010-1234-5678 형식으로 들어가서
    OAuth VARCHAR(20) CHECK (OAuth IN ('google','naver','kakao')),
    role VARCHAR(20) CHECK (role IN ('customer','admin')),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    key_parent VARCHAR(100) default null  --부모인증키
);

--diary (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS diary(
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    text TEXT,
    user_id INT,
    CONSTRAINT fk_diary_user FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
    );

-- 독후감 (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS reading_logs (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP, -- 수정 날짜, null 가능
    book_title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publisher VARCHAR(255),
    content VARCHAR(200), -- 독서록 내용, 200자
    unknown_sentence TEXT -- 모르는 문장 인용
    );

-- 생활글쓰기(일기) (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS daily_writings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    content TEXT NOT NULL,
    attachment_url VARCHAR(255) -- 첨부파일 경로
);

-- 독서토론 (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS reading_forum_posts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    book_title VARCHAR(255), -- 관련 도서
    discussion_tags VARCHAR(100) -- 토론 주제 태그
);

-- 부모 커뮤니티 (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS parent_forum_posts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    category VARCHAR(50), -- 예: 교육, 육아, 상담
    is_important BOOLEAN DEFAULT FALSE -- 공지 여부
);

-- 테스트 (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS user_tests (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    test_type VARCHAR(50) CHECK (test_type IN ('literacy', 'vocabulary')), -- 문해력, 어휘력
    taken_at TIMESTAMP DEFAULT NOW(), -- 시험 응시 날짜
    questions JSONB NOT NULL,         -- 문제와 답을 JSON으로 저장
    user_answers JSONB,               -- 사용자가 선택한 답을 JSON으로 저장
    total_score INT                   -- 총 점수
    );

-- 게임 (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS user_games (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    game_type VARCHAR(50) CHECK (game_type IN ('word_chain','word_meaning','sentence_completion')), -- 끝말잇기, 단어 뜻 맞추기, 문장 완성
    played_at TIMESTAMP DEFAULT NOW(), -- 게임 플레이 날짜
    score INT                         -- 유저 점수
);

-- 구독권 (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE, -- 사용자와 연결
    plan_name VARCHAR(50) NOT NULL,                    -- 플랜 이름 (예: Basic, Premium)
    status VARCHAR(20) CHECK (status IN ('active','expired','canceled')) DEFAULT 'active',
    start_date TIMESTAMP NOT NULL,                     -- 구독 시작일
    end_date TIMESTAMP NOT NULL,                       -- 구독 종료일
    created_at TIMESTAMP DEFAULT NOW(),               -- 레코드 생성 시각
    updated_at TIMESTAMP DEFAULT NOW()                -- 레코드 수정 시각
    );

-- 고객센터 게시판 (질문+답변 쓰레드 구조) (JOIN 가능: users, 자기참조 가능: parent_id)
CREATE TABLE IF NOT EXISTS customer_support (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    parent_id INT REFERENCES customer_support(id) ON DELETE CASCADE, -- null이면 질문, 값이 있으면 답변/댓글
    category VARCHAR(50),
    title VARCHAR(255),
    content TEXT,
    status VARCHAR(20) CHECK (status IN ('open','in_progress','resolved','closed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
    );

-- words (JOIN 가능: user_word_usage)
CREATE TABLE IF NOT EXISTS words (
    word_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    word_text TEXT NOT NULL UNIQUE,
    definition TEXT,
    synonyms TEXT[],
    embedding FLOAT8[]
    );

-- outputs (JOIN 가능: users)
CREATE TABLE IF NOT EXISTS outputs (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    source TEXT,
    content_summary JSONB
    );

-- user_word_usage (JOIN 가능: outputs, words)
CREATE TABLE IF NOT EXISTS user_word_usage (
    usage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id UUID REFERENCES outputs(record_id) ON DELETE CASCADE,
    word_id UUID REFERENCES words(word_id) ON DELETE CASCADE,
    frequency INT,
    user_embedding FLOAT8[]
);