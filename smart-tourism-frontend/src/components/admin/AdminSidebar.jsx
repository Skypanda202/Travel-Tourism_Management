import {
  FaChartBar,
  FaMapMarkedAlt,
  FaUsers,
  FaTaxi,
  FaStar,
  FaMoneyBill,
  FaClipboardList,
} from "react-icons/fa";

import { Link } from "react-router-dom";

const AdminSidebar = () => {
  return (
    <div
      className="bg-dark text-light p-4"
      style={{
        width: "280px",
        minHeight: "100vh",
      }}
    >
      <h3 className="mb-5 fw-bold">
        Admin Panel
      </h3>

      <ul className="list-unstyled">
        <li className="mb-4">
          <Link
            to="/admin"
            className="text-light text-decoration-none"
          >
            <FaChartBar className="me-2" />
            Dashboard
          </Link>
        </li>

        <li className="mb-4">
          <Link
            to="/admin/places"
            className="text-light text-decoration-none"
          >
            <FaMapMarkedAlt className="me-2" />
            Tourist Places
          </Link>
        </li>

        <li className="mb-4">
          <Link
            to="/admin/bookings"
            className="text-light text-decoration-none"
          >
            <FaClipboardList className="me-2" />
            Bookings
          </Link>
        </li>

        <li className="mb-4">
          <Link
            to="/admin/cabs"
            className="text-light text-decoration-none"
          >
            <FaTaxi className="me-2" />
            Cab Management
          </Link>
        </li>

        <li className="mb-4">
          <Link
            to="/admin/users"
            className="text-light text-decoration-none"
          >
            <FaUsers className="me-2" />
            Users
          </Link>
        </li>

        <li className="mb-4">
          <Link
            to="/admin/reviews"
            className="text-light text-decoration-none"
          >
            <FaStar className="me-2" />
            Reviews
          </Link>
        </li>

        <li className="mb-4">
          <Link
            to="/admin/revenue"
            className="text-light text-decoration-none"
          >
            <FaMoneyBill className="me-2" />
            Revenue
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default AdminSidebar;