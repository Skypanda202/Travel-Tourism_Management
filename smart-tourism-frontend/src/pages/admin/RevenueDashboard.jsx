import {
  Container,
  Row,
  Col,
  Card,
} from "react-bootstrap";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const revenueData = [
  { month: "Jan", revenue: 120000 },
  { month: "Feb", revenue: 180000 },
  { month: "Mar", revenue: 250000 },
  { month: "Apr", revenue: 300000 },
  { month: "May", revenue: 450000 },
];

const RevenueDashboard = () => {
  return (
    <Container fluid>
      <h2 className="fw-bold mb-4">
        Revenue Dashboard
      </h2>

      <Row className="mb-4">
        <Col md={4}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h5>Total Revenue</h5>

            <h2>₹13,00,000</h2>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h5>Monthly Growth</h5>

            <h2>+18%</h2>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h5>Total Transactions</h5>

            <h2>3,250</h2>
          </Card>
        </Col>
      </Row>

      <Card className="shadow border-0 rounded-4 p-4">
        <h4 className="mb-4">
          Revenue Overview
        </h4>

        <ResponsiveContainer
          width="100%"
          height={400}
        >
          <LineChart data={revenueData}>
            <XAxis dataKey="month" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="revenue"
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>
    </Container>
  );
};

export default RevenueDashboard;