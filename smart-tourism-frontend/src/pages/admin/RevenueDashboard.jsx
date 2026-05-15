import { useEffect, useState } from "react";
import { Alert, Col, Row, Spinner, Table } from "react-bootstrap";
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import axiosInstance from "../../api/axiosInstance";

const RevenueDashboard = () => {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchRevenue = async () => {
      try {
        setLoading(true);
        setError("");
        const response = await axiosInstance.get("analytics/revenue/");
        setReport(response.data.data || null);
      } catch (fetchError) {
        console.log(fetchError);
        setError("Could not load revenue analytics.");
      } finally {
        setLoading(false);
      }
    };

    fetchRevenue();
  }, []);

  if (loading) {
    return (
      <div className="loading-wrap">
        <Spinner animation="border" role="status" />
      </div>
    );
  }

  const dailyTrend = report?.daily_trend || [];
  const byMethod = report?.by_method || [];

  return (
    <div>
      <span className="section-eyebrow">Admin revenue</span>
      <h1 className="h2 fw-bold mt-2 mb-4">Revenue</h1>

      {error ? <Alert variant="warning">{error}</Alert> : null}

      <Row className="g-4 mb-4">
        <Col md={4}>
          <div className="feature-card">
            <h2 className="h5 fw-bold">Total revenue</h2>
            <p className="display-6 fw-bold mb-0">
              Rs {Number(report?.total_revenue || 0).toLocaleString("en-IN")}
            </p>
          </div>
        </Col>
        <Col md={4}>
          <div className="feature-card">
            <h2 className="h5 fw-bold">Tour bookings</h2>
            <p className="display-6 fw-bold mb-0">
              Rs {Number(report?.booking_revenue || 0).toLocaleString("en-IN")}
            </p>
          </div>
        </Col>
        <Col md={4}>
          <div className="feature-card">
            <h2 className="h5 fw-bold">Cab bookings</h2>
            <p className="display-6 fw-bold mb-0">
              Rs {Number(report?.cab_revenue || 0).toLocaleString("en-IN")}
            </p>
          </div>
        </Col>
      </Row>

      <div className="detail-panel mb-4">
        <h2 className="h4 fw-bold">Daily trend</h2>
        {dailyTrend.length ? (
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={dailyTrend}>
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#176b4f" />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <div className="empty-state">
            Revenue trend will appear after successful payments are recorded.
          </div>
        )}
      </div>

      <div className="detail-panel">
        <h2 className="h4 fw-bold">Payment methods</h2>
        {byMethod.length ? (
          <Table responsive hover>
            <thead>
              <tr>
                <th>Method</th>
                <th>Transactions</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {byMethod.map((row) => (
                <tr key={row.payment_method || "unknown"}>
                  <td>{row.payment_method || "Unknown"}</td>
                  <td>{row.count}</td>
                  <td>Rs {Number(row.amount || 0).toLocaleString("en-IN")}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        ) : (
          <div className="empty-state">
            No successful payment methods have been recorded yet.
          </div>
        )}
      </div>
    </div>
  );
};

export default RevenueDashboard;
