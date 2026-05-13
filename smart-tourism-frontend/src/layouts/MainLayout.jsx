import NavigationBar from "../components/navbar/Navbar";
import Footer from "../components/footer/Footer";

const MainLayout = ({ children }) => {
  return (
    <>
      <NavigationBar />

      <main>{children}</main>

      <Footer />
    </>
  );
};

export default MainLayout;