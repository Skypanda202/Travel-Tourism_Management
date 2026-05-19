import { useContext, useEffect, useState } from "react";
import { Alert, Button, Col, Container, Row, Spinner } from "react-bootstrap";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import { FaCalendarAlt, FaHeart, FaMapMarkedAlt, FaStar } from "react-icons/fa";
import axiosInstance from "../../api/axiosInstance";
import AuthContext from "../../context/authContextValue";

const statCards = [
  { key: "total_bookings", label: "Total bookings", icon: FaCalendarAlt },
  { key: "upcoming_bookings", label: "Upcoming trips", icon: FaMapMarkedAlt },
  { key: "saved_places", label: "Saved places", icon: FaHeart },
  { key: "total_reviews", label: "Reviews", icon: FaStar },
];

const UserDashboard = () => {
  const { logout } = useContext(AuthContext);
  const [stats, setStats] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true);
        setError("");
        const [dashboardResponse, profileResponse] = await Promise.all([
          axiosInstance.get("users/dashboard/"),
          axiosInstance.get("users/profile/"),
        ]);

        setStats(dashboardResponse.data.data || {});
        setProfile(profileResponse.data.data || null);
      } catch (fetchError) {
        console.log(fetchError);
        setError("Could not load your account details. Please login again.");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  const resendVerification = async () => {
    try {
      await axiosInstance.post("resend-verification/");
      toast.success("Verification email sent");
    } catch (verifyError) {
      console.log(verifyError);
      toast.error("Could not send verification email");
    }
  };

  const deleteAccount = async () => {
    const confirmed = window.confirm("Delete your account? You will be logged out and your account will be deactivated.");
    if (!confirmed) {
      return;
    }

    try {
      await axiosInstance.delete("users/delete-account/");
      logout();
      toast.success("Account deactivated");
      window.location.href = "/";
    } catch (deleteError) {
      console.log(deleteError);
      toast.error("Could not delete your account");
    }
  };

  if (loading) {
    return (
      <div className="loading-wrap">
        <Spinner animation="border" role="status" />
      </div>
    );
  }

  return (
    <section className="section-band">
      <Container>
        <Row className="align-items-end mb-4 g-3">
          <Col lg={8}>
            <span className="section-eyebrow">Visitor account</span>
            <h1 className="section-title">My account</h1>
            <p className="section-copy">
              {profile?.full_name || profile?.email
                ? `Welcome${profile.full_name ? `, ${profile.full_name}` : ""}.`
                : "Your trip activity appears here after you start using the app."}
            </p>
          </Col>

          <Col lg={4} className="text-lg-end">
            <Button as={Link} to="/profile" className="btn-outline-soft me-2 mb-2">
              Edit profile
            </Button>
            <Button as={Link} to="/places" className="btn-primary-soft me-2 mb-2">
              Explore places
            </Button>
            <Button as={Link} to="/favorites" className="btn-outline-soft mb-2">
              Favorites
            </Button>
          </Col>
        </Row>

        {error ? <Alert variant="warning">{error}</Alert> : null}
        {profile && !profile.is_verified ? (
          <Alert variant="warning" className="d-flex flex-wrap align-items-center justify-content-between gap-2">
            <span>Please verify your email to keep your account secure.</span>
            <Button className="btn-outline-soft btn-sm" onClick={resendVerification}>
              Resend email
            </Button>
          </Alert>
        ) : null}

        <Row className="g-4">
          {statCards.map(({ key, label, icon: Icon }) => (
            <Col md={6} lg={3} key={key}>
              <div className="feature-card">
                <span className="feature-icon mb-3">
                  <Icon />
                </span>
                <h2 className="h5 fw-bold">{label}</h2>
                <p className="display-6 fw-bold mb-0">{stats?.[key] ?? 0}</p>
              </div>
            </Col>
          ))}
        </Row>

        <div className="detail-panel mt-4">
          <h2 className="h4 fw-bold">Next steps</h2>
          <p className="section-copy mb-3">
            Browse tourist places, save favorites, or book a cab when you are
            ready to plan a visit.
          </p>
          <div className="d-flex flex-wrap gap-2">
            <Button as={Link} to="/places" className="btn-primary-soft">
              Browse places
            </Button>
            <Button as={Link} to="/cab-booking" className="btn-outline-soft">
              Book cab
            </Button>
            <Button as={Link} to="/profile" className="btn-outline-soft">
              Update profile
            </Button>
          </div>
        </div>

        <div className="detail-panel mt-4">
          <h2 className="h4 fw-bold">Account controls</h2>
          <p className="section-copy mb-3">
            Deleting your account deactivates login access while preserving booking and review history for admin records.
          </p>
          <Button variant="danger" onClick={deleteAccount}>
            Delete my account
          </Button>
        </div>
      </Container>
    </section>
  );
};

export default UserDashboard;
