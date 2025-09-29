import { createBrowserRouter } from "react-router-dom";

// 메인 페이지
import MainPage from "../pages/Main/MainPage";

// 활동
import ReadingLogPage from "../pages/Activity/ReadingLog/ReadingLogPage";
import DailyWritingPage from "../pages/Activity/DailyWriting/DailyWritingPage";
import WordSearchPage from "../pages/Activity/WordSearch/WordSearchPage";

// 커뮤니티
import StudentDiscussionPage from "../pages/Community/StudentDiscussion/StudentDiscussionPage";
import ParentBoardPage from "../pages/Community/ParentBoard/ParentBoardPage";

// AI와 대화
import AIChatPage from "../pages/AIChat/AIChatPage";

// 테스트
import LiteracyTestPage from "../pages/Tests/LiteracyTest/LiteracyTestPage";
import VocabularyTestPage from "../pages/Tests/VocabularyTest/VocabularyTestPage";

// 게임
import WordChainPage from "../pages/Games/WordChain/WordChainPage";
import WordMeaningPage from "../pages/Games/WordMeaning/WordMeaningPage";
import SentenceCompletePage from "../pages/Games/SentenceComplete/SentenceCompletePage";

// 마이페이지
import DashboardPage from "../pages/MyPage/Dashboard/DashboardPage";
import ProfileEditPage from "../pages/MyPage/ProfileEdit/ProfileEditPage";
import SubscriptionPage from "../pages/MyPage/Subscription/SubscriptionPage";

// 로그인/회원 관련
import LoginPage from "../pages/Auth/Login/LoginPage";
import RegisterPage from "../pages/Auth/Register/RegisterPage";
import FindAccountPage from "../pages/Auth/FindAccount/FindAccountPage";
import WithdrawPage from "../pages/Auth/Withdraw/WithdrawPage";

// 레이아웃
import MainLayout from "../layouts/MainLayout";

const router = createBrowserRouter([
    {
        path: "/",
        element: (
            <MainLayout>
                <MainPage />
            </MainLayout>
        ),
    },
    // 활동
    {
        path: "/activity/reading-log",
        element: (
            <MainLayout>
                <ReadingLogPage />
            </MainLayout>
        ),
    },
    {
        path: "/activity/daily-writing",
        element: (
            <MainLayout>
                <DailyWritingPage />
            </MainLayout>
        ),
    },
    {
        path: "/activity/word-search",
        element: (
            <MainLayout>
                <WordSearchPage />
            </MainLayout>
        ),
    },
    // 커뮤니티
    {
        path: "/community/student-discussion",
        element: (
            <MainLayout>
                <StudentDiscussionPage />
            </MainLayout>
        ),
    },
    {
        path: "/community/parent-board",
        element: (
            <MainLayout>
                <ParentBoardPage />
            </MainLayout>
        ),
    },
    // AI와 대화
    {
        path: "/ai-chat",
        element: (
            <MainLayout>
                <AIChatPage />
            </MainLayout>
        ),
    },
    // 테스트
    {
        path: "/tests/literacy",
        element: (
            <MainLayout>
                <LiteracyTestPage />
            </MainLayout>
        ),
    },
    {
        path: "/tests/vocabulary",
        element: (
            <MainLayout>
                <VocabularyTestPage />
            </MainLayout>
        ),
    },
    // 게임
    {
        path: "/games/word-chain",
        element: (
            <MainLayout>
                <WordChainPage />
            </MainLayout>
        ),
    },
    {
        path: "/games/word-meaning",
        element: (
            <MainLayout>
                <WordMeaningPage />
            </MainLayout>
        ),
    },
    {
        path: "/games/sentence-complete",
        element: (
            <MainLayout>
                <SentenceCompletePage />
            </MainLayout>
        ),
    },
    // 마이페이지
    {
        path: "/mypage/dashboard",
        element: (
            <MainLayout>
                <DashboardPage />
            </MainLayout>
        ),
    },
    {
        path: "/mypage/profile-edit",
        element: (
            <MainLayout>
                <ProfileEditPage />
            </MainLayout>
        ),
    },
    {
        path: "/mypage/subscription",
        element: (
            <MainLayout>
                <SubscriptionPage />
            </MainLayout>
        ),
    },
    // 인증(Auth)
    {
        path: "/login",
        element: (
            <MainLayout>
                <LoginPage />
            </MainLayout>
        ),
    },
    {
        path: "/register",
        element: (
            <MainLayout>
                <RegisterPage />
            </MainLayout>
        ),
    },
    {
        path: "/find-account",
        element: (
            <MainLayout>
                <FindAccountPage />
            </MainLayout>
        ),
    },
    {
        path: "/withdraw",
        element: (
            <MainLayout>
                <WithdrawPage />
            </MainLayout>
        ),
    },
]);

export default router;
