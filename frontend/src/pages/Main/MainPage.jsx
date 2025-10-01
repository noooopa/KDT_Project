import { Link } from "react-router-dom";
import logoImg from "../../assets/logo.png";
import treasureMap from "../../assets/treasure-map.JPG";

function MainPage() {
    return (
        <div className="space-y-20">
            {/* Hero Section */}
            <section className="text-center py-24 bg-gradient-to-t from-primary to-white rounded-xl">
                <div className="flex flex-col items-center">
                    <img src={logoImg} alt="새싹톡 로고" className="h-40 mb-6" />
                    <p className="text-lg md:text-xl font-main text-textsub">
                        아동·청소년 어휘력 증진을 위한 인공지능 학습 플랫폼
                    </p>
                </div>
            </section>

            {/* 보물지도 네비게이션 */}
            <section
                className="relative w-full aspect-square bg-cover bg-center rounded-xl shadow-lg"
                style={{ backgroundImage: `url(${treasureMap})` }}
            >
                {/* 활동 */}
                <Link
                    to="/activity"
                    className="group absolute top-24 left-40 w-20 h-20 flex items-center justify-center"
                >
                    <div className="text-5xl group-hover:hidden">📚</div>
                    <div className="
            hidden group-hover:flex flex-col items-center justify-center
            absolute -top-10 left-1/2 -translate-x-1/2
            w-96 h-40 p-6 rounded-2xl shadow-2xl
            bg-secondary text-white animate-pop-bounce
          ">
                        <h3 className="text-2xl font-bold mb-2">활동</h3>
                        <ul className="text-base flex gap-4">
                            <li>독서록</li>
                            <li>생활 글쓰기</li>
                            <li>어휘 검색</li>
                        </ul>
                        <p className="mt-2 text-sm">다양한 활동으로 어휘력을 확장하세요!</p>
                    </div>
                </Link>

                {/* 커뮤니티 */}
                <Link
                    to="/community"
                    className="group absolute top-1/3 right-52 w-20 h-20 flex items-center justify-center"
                >
                    <div className="text-5xl group-hover:hidden">👥</div>
                    <div className="
            hidden group-hover:flex flex-col items-center justify-center
            absolute -top-10 left-1/2 -translate-x-1/2
            w-96 h-40 p-6 rounded-2xl shadow-2xl
            bg-accent text-white animate-pop-bounce
          ">
                        <h3 className="text-2xl font-bold mb-2">커뮤니티</h3>
                        <ul className="text-base flex gap-4">
                            <li>독서토론(학생)</li>
                            <li>부모 커뮤니티</li>
                        </ul>
                        <p className="mt-2 text-sm">서로의 생각을 나누는 소통 공간</p>
                    </div>
                </Link>

                {/* 테스트 */}
                <Link
                    to="/tests"
                    className="group absolute bottom-32 left-1/4 w-20 h-20 flex items-center justify-center"
                >
                    <div className="text-5xl group-hover:hidden">📝</div>
                    <div className="
            hidden group-hover:flex flex-col items-center justify-center
            absolute -top-10 left-1/2 -translate-x-1/2
            w-96 h-40 p-6 rounded-2xl shadow-2xl
            bg-darkgreen text-white animate-pop-bounce
          ">
                        <h3 className="text-2xl font-bold mb-2">테스트</h3>
                        <ul className="text-base flex gap-4">
                            <li>문해력 테스트</li>
                            <li>어휘력 테스트</li>
                        </ul>
                        <p className="mt-2 text-sm">실력을 점검하고 성장하세요!</p>
                    </div>
                </Link>

                {/* 게임 */}
                <Link
                    to="/games"
                    className="group absolute bottom-20 right-40 w-20 h-20 flex items-center justify-center"
                >
                    <div className="text-5xl group-hover:hidden">🎮</div>
                    <div className="
            hidden group-hover:flex flex-col items-center justify-center
            absolute -top-10 left-1/2 -translate-x-1/2
            w-96 h-40 p-6 rounded-2xl shadow-2xl
            bg-primary text-darkgreen animate-pop-bounce
          ">
                        <h3 className="text-2xl font-bold mb-2">게임</h3>
                        <ul className="text-base flex gap-4">
                            <li>끝말잇기</li>
                            <li>단어 맞추기</li>
                            <li>문장 완성하기</li>
                        </ul>
                        <p className="mt-2 text-sm">즐겁게 배우는 어휘 게임!</p>
                    </div>
                </Link>
            </section>
        </div>
    );
}

export default MainPage;
