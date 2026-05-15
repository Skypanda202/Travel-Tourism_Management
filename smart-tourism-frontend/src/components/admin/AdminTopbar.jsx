import { useContext } from "react";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import AuthContext from "../../context/authContextValue";

const AdminTopbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="bg-white shadow-sm p-3 d-flex justify-content-between align-items-center">
      <div>
        <h4 className="fw-bold mb-0">Smart Tourism Admin</h4>
        <small className="text-secondary">
          {user?.email || user?.full_name || "Admin account"}
        </small>
      </div>

      <Button
        type="button"
        className="btn-outline-soft"
        onClick={handleLogout}
      >
        Logout
      </Button>
    </div>
  );
};

export default AdminTopbar;
