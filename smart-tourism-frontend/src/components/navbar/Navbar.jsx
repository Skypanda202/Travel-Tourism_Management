import { Button, Container, Nav, Navbar } from "react-bootstrap";
import { useContext } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import {
  FaChartLine,
  FaComments,
  FaHeart,
  FaMapMarkedAlt,
  FaPlusCircle,
  FaUserCircle,
} from "react-icons/fa";
import AuthContext from "../../context/authContextValue";

const NavigationBar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const isAdmin = user?.is_admin || user?.role === "admin";

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Navbar className="site-navbar" expand="lg" sticky="top">
      <Container>
        <Navbar.Brand
          as={Link}
          to="/"
          className="d-flex align-items-center gap-2 fw-bold"
        >
          <span className="brand-mark">ST</span>
          <span>Smart Tourism</span>
        </Navbar.Brand>

        <Navbar.Toggle aria-controls="main-navbar" />

        <Navbar.Collapse id="main-navbar">
          <Nav className="mx-auto align-items-lg-center gap-lg-2">
            <Nav.Link as={NavLink} to="/">
              Home
            </Nav.Link>

            <Nav.Link as={NavLink} to="/places">
              Places
            </Nav.Link>

            <Nav.Link as={NavLink} to="/maps">
              <FaMapMarkedAlt className="me-1" />
              Map
            </Nav.Link>

            <Nav.Link as={NavLink} to="/assistant">
              <FaComments className="me-1" />
              Assistant
            </Nav.Link>

            {isAdmin ? (
              <>
                <Nav.Link as={NavLink} to="/admin">
                  <FaUserCircle className="me-1" />
                  Admin
                </Nav.Link>

                <Nav.Link as={NavLink} to="/admin/places">
                  <FaPlusCircle className="me-1" />
                  Add details
                </Nav.Link>

                <Nav.Link as={NavLink} to="/admin/revenue">
                  <FaChartLine className="me-1" />
                  Revenue
                </Nav.Link>
              </>
            ) : user ? (
              <>
                <Nav.Link as={NavLink} to="/dashboard">
                  <FaUserCircle className="me-1" />
                  My account
                </Nav.Link>

                <Nav.Link as={NavLink} to="/favorites">
                  <FaHeart className="me-1" />
                  Favorites
                </Nav.Link>
              </>
            ) : null}
          </Nav>

          <Nav className="ms-lg-auto align-items-lg-center gap-2">
            {user ? (
              <Button
                type="button"
                className="nav-action btn-outline-soft"
                onClick={handleLogout}
              >
                Logout
              </Button>
            ) : (
              <>
                <Button as={Link} to="/login" className="nav-action btn-outline-soft">
                  Visitor login
                </Button>

                <Button as={Link} to="/register" className="nav-action btn-primary-soft">
                  Visitor sign up
                </Button>
              </>
            )}

          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
