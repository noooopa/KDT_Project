import Header from "./Header";
import Footer from "./Footer";

function MainLayout({ children }) {
    return (
        <div className="flex flex-col min-h-screen">
            <Header />
            <main
                className="
          flex-grow
          px-4
          md:px-8
          lg:px-20
          2xl:px-[300px]
        "
            >
                {children}
            </main>
            <Footer />
        </div>
    );
}

export default MainLayout;
