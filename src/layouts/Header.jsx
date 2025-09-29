import { Link } from "react-router-dom";

function Header() {
    return (
        <header className="flex justify-between items-center px-6 py-4">
            {/* 로고 */}
            <h1 className="font-logo text-2xl">
                <Link to="/">새싹톡 🌱</Link>
            </h1>

            {/* 네비게이션 */}
            <nav className="space-x-4 font-main">
                {/* 메인 */}
                <Link to="/">메인</Link>

                {/* 활동 */}
                <Link to="/activity/reading-log">독서록</Link>
                <Link to="/activity/daily-writing">생활 글쓰기</Link>
                <Link to="/activity/word-search">어휘 검색</Link>

                {/* 커뮤니티 */}
                <Link to="/community/student-discussion">독서토론</Link>
                <Link to="/community/parent-board">부모 커뮤니티</Link>

                {/* 테스트 */}
                <Link to="/tests/literacy">문해력 테스트</Link>
                <Link to="/tests/vocabulary">어휘력 테스트</Link>

                {/* 게임 */}
                <Link to="/games/word-chain">끝말잇기</Link>
                <Link to="/games/word-meaning">단어 뜻 맞추기</Link>
                <Link to="/games/sentence-complete">문장 완성하기</Link>

                {/* 마이페이지 */}
                <Link to="/mypage/dashboard">마이페이지</Link>

                {/* 로그인 */}
                <Link to="/login">로그인</Link>
            </nav>
        </header>
    );
}

export default Header;
