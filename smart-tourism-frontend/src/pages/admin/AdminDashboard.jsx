import {
  Container,
  Row,
  Col,
  Card,
  Table,
} from "react-bootstrap";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { month: "Jan", users: 400 },
  { month: "Feb", users: 700 },
  { month: "Mar", users: 1200 },
  { month: "Apr", users: 950 },
];

const AdminDashboard = () => {
  return (
    <Container fluid>
      <h2 className="mb-4 fw-bold">
        Dashboard Analytics
      </h2>

      {/* Stats */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h5>Total Visitors</h5>
            <h2>25,450</h2>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h5>Total Revenue</h5>
            <h2>₹8,50,000</h2>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h5>Total Bookings</h5>
            <h2>1,240</h2>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h5>Cab Bookings</h5>
            <h2>350</h2>
          </Card>
        </Col>
      </Row>

      {/* Charts */}
      <Row>
        <Col md={8}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h4 className="mb-4">
              Monthly Visitors
            </h4>

            <ResponsiveContainer
              width="100%"
              height={300}
            >
              <BarChart data={data}>
                <XAxis dataKey="month" />

                <YAxis />

                <Tooltip />

                <Bar dataKey="users" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="shadow border-0 rounded-4 p-4">
            <h4>Top Destination</h4>

            <img
              src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
              alt="destination"
              className="img-fluid rounded-4 mt-3"
            />
          </Card>
        </Col>
      </Row>

      {/* Recent Bookings */}
      <Card className="shadow border-0 rounded-4 p-4 mt-4">
        <h4 className="mb-4">
          Recent Bookings
        </h4>

        <Table responsive hover>
          <thead>
            <tr>
              <th>User</th>
              <th>Destination</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Akash</td>
              <td>Goa</td>
              <td>Confirmed</td>
            </tr>

            <tr>
              <td>Rahul</td>
              <td>Manali</td>
              <td>Pending</td>
            </tr>
          </tbody>
        </Table>
      </Card>
    </Container>
  );
};

export default AdminDashboard;