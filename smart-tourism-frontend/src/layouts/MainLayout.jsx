import NavigationBar from "../components/navbar/Navbar";
import Footer from "../components/footer/Footer";

const MainLayout = ({ children }) => {
  return (
    <div className="app-shell">
      <NavigationBar />
      <main className="app-main">{children}</main>
      <Footer />
    </div>
  );
};

export default MainLayout;
