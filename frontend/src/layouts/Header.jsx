import { Link } from "react-router-dom";
import { useState } from "react";
import logoImg from "../assets/logo.png";

function Header() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return (
        <header className="bg-white">
            <div
                className="
          flex items-end justify-between
          px-4
          md:px-8
          lg:px-20
          2xl:px-[300px]
        "
            >
                {/* 로고 */}
                <Link to="/" className="flex items-end">
                    <img src={logoImg} alt="새싹톡 로고" className="h-28 mr-2" />
                </Link>

                {/* 메뉴 */}
                <nav className="flex space-x-8 md:space-x-10 font-main text-base md:text-lg lg:text-xl items-end font-semibold">
                    <Link to="/activity" className="hover:text-darkgreen">활동</Link>
                    <Link to="/community" className="hover:text-darkgreen">커뮤니티</Link>
                    <Link to="/tests" className="hover:text-darkgreen">테스트</Link>
                    <Link to="/games" className="hover:text-darkgreen">게임</Link>
                    {isLoggedIn ? (
                        <Link to="/mypage" className="hover:text-darkgreen">마이페이지</Link>
                    ) : (
                        <Link to="/login" className="hover:text-darkgreen">로그인</Link>
                    )}
                </nav>
            </div>
        </header>
    );
}

export default Header;
