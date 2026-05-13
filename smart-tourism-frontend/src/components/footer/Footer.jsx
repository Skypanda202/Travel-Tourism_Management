import {
  FaFacebook,
  FaInstagram,
  FaTwitter,
  FaYoutube,
} from "react-icons/fa";

const Footer = () => {
  return (
    <footer className="bg-dark text-light pt-5 pb-3">
      <div className="container">
        <div className="row">
          {/* Brand */}
          <div className="col-md-4 mb-4">
            <h3 className="fw-bold">Smart Tourism</h3>

            <p>
              Explore the world with intelligent tourism
              management solutions.
            </p>
          </div>

          {/* Quick Links */}
          <div className="col-md-4 mb-4">
            <h5>Quick Links</h5>

            <ul className="list-unstyled">
              <li>Home</li>
              <li>Places</li>
              <li>Bookings</li>
              <li>Contact</li>
            </ul>
          </div>

          {/* Social */}
          <div className="col-md-4 mb-4">
            <h5>Follow Us</h5>

            <div className="d-flex gap-3 fs-4">
              <FaFacebook />
              <FaInstagram />
              <FaTwitter />
              <FaYoutube />
            </div>
          </div>
        </div>

        <hr />

        <p className="text-center mb-0">
          © 2026 Smart Tourism Management System
        </p>
      </div>
    </footer>
  );
};

export default Footer;