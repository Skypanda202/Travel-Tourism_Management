import { FaFacebook, FaInstagram, FaTwitter, FaYoutube } from "react-icons/fa";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="site-footer pt-5 pb-3">
      <div className="container">
        <div className="row g-4">
          <div className="col-md-4 mb-4">
            <h3 className="fw-bold text-white">Smart Tourism</h3>
            <p>
              Plan better trips across Kalahandi and Odisha with places, maps,
              bookings, and a travel assistant in one friendly space.
            </p>
          </div>

          <div className="col-md-3 mb-4">
            <h5 className="text-white">Explore</h5>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link to="/">Home</Link>
              </li>
              <li className="mb-2">
                <Link to="/places">Places</Link>
              </li>
              <li className="mb-2">
                <Link to="/maps">Map</Link>
              </li>
              <li className="mb-2">
                <Link to="/assistant">Assistant</Link>
              </li>
            </ul>
          </div>

          <div className="col-md-2 mb-4">
            <h5 className="text-white">Visitor</h5>
            <ul className="list-unstyled">
              <li className="mb-2">
                <Link to="/login">Visitor login</Link>
              </li>
              <li className="mb-2">
                <Link to="/register">Visitor sign up</Link>
              </li>
              <li className="mb-2">
                <Link to="/dashboard">Visitor page</Link>
              </li>
              <li className="mb-2">
                <Link to="/admin">Admin login</Link>
              </li>
              <li className="mb-2">
                <Link to="/admin/places">Admin panel</Link>
              </li>
            </ul>
          </div>

          <div className="col-md-3 mb-4">
            <h5 className="text-white">Follow Us</h5>
            <div className="d-flex gap-3 fs-4">
              <span className="footer-social">
                <FaFacebook />
              </span>
              <span className="footer-social">
                <FaInstagram />
              </span>
              <span className="footer-social">
                <FaTwitter />
              </span>
              <span className="footer-social">
                <FaYoutube />
              </span>
            </div>
          </div>
        </div>

        <hr />

        <p className="text-center mb-0">2026 Smart Tourism Management System</p>
      </div>
    </footer>
  );
};

export default Footer;
