import { useEffect, useState } from "react";
import { Alert, Col, Row, Spinner } from "react-bootstrap";
import { FaCalendarCheck, FaMapMarkedAlt, FaRupeeSign, FaUsers } from "react-icons/fa";
import axiosInstance from "../../api/axiosInstance";

const kpiCards = [
  { key: "total_users", label: "Visitors", icon: FaUsers },
  { key: "total_places", label: "Published places", icon: FaMapMarkedAlt },
  { key: "total_bookings", label: "Bookings", icon: FaCalendarCheck },
  { key: "revenue_total", label: "Total revenue", icon: FaRupeeSign, currency: true },
];

const AdminDashboard = () => {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true);
        setError("");
        const response = await axiosInstance.get("analytics/dashboard/");
        setKpis(response.data.data || {});
      } catch (fetchError) {
        console.log(fetchError);
        setError("Could not load admin analytics.");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="loading-wrap">
        <Spinner animation="border" role="status" />
      </div>
    );
  }

  return (
    <div>
      <span className="section-eyebrow">Admin overview</span>
      <h1 className="h2 fw-bold mt-2 mb-4">Dashboard</h1>

      {error ? <Alert variant="warning">{error}</Alert> : null}

      <Row className="g-4 mb-4">
        {kpiCards.map(({ key, label, icon: Icon, currency }) => (
          <Col md={6} xl={3} key={key}>
            <div className="feature-card">
              <span className="feature-icon mb-3">
                <Icon />
              </span>
              <h2 className="h5 fw-bold">{label}</h2>
              <p className="display-6 fw-bold mb-0">
                {currency ? `Rs ${Number(kpis?.[key] || 0).toLocaleString("en-IN")}` : kpis?.[key] || 0}
              </p>
            </div>
          </Col>
        ))}
      </Row>

      <Row className="g-4">
        <Col lg={6}>
          <div className="detail-panel h-100">
            <h2 className="h4 fw-bold">This month</h2>
            <p className="section-copy mb-3">Live monthly activity from the database.</p>
            <div className="d-grid gap-2">
              <span>New users: {kpis?.new_users_this_month || 0}</span>
              <span>Bookings: {kpis?.bookings_this_month || 0}</span>
              <span>Revenue: Rs {Number(kpis?.revenue_this_month || 0).toLocaleString("en-IN")}</span>
            </div>
          </div>
        </Col>

        <Col lg={6}>
          <div className="detail-panel h-100">
            <h2 className="h4 fw-bold">Review queue</h2>
            <p className="section-copy mb-3">Moderation and quality signals.</p>
            <div className="d-grid gap-2">
              <span>Approved reviews: {kpis?.total_reviews || 0}</span>
              <span>Pending reviews: {kpis?.pending_reviews || 0}</span>
              <span>Average rating: {Number(kpis?.avg_platform_rating || 0).toFixed(1)}</span>
            </div>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default AdminDashboard;
