import {
  Navbar,
  Nav,
  Container,
  Button,
} from "react-bootstrap";

import { Link } from "react-router-dom";

import {
  FaUserCircle,
  FaRobot,
} from "react-icons/fa";

const NavigationBar = () => {
  return (
    <Navbar
      bg="dark"
      variant="dark"
      expand="lg"
      sticky="top"
    >
      <Container>
        <Navbar.Brand as={Link} to="/">
          Smart Tourism
        </Navbar.Brand>

        <Navbar.Toggle />

        <Navbar.Collapse>
          <Nav className="ms-auto align-items-center">

            <Nav.Link as={Link} to="/">
              Home
            </Nav.Link>

            <Nav.Link as={Link} to="/places">
              Places
            </Nav.Link>

            {/* Login Button */}
            <Button
              as={Link}
              to="/login"
              variant="outline-light"
              className="me-2"
            >
              Login
            </Button>

            {/* Register */}
            <Button
              as={Link}
              to="/register"
              variant="warning"
            >
              Register
            </Button>

            {/* User Icon */}
            <FaUserCircle
              size={28}
              className="ms-3"
            />
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;