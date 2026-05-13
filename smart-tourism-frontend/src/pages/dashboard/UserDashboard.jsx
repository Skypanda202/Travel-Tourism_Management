import {
  Container,
  Row,
  Col,
  Card,
  Table,
  Badge,
} from "react-bootstrap";

import {
  FaMapMarkedAlt,
  FaHeart,
  FaTaxi,
  FaCalendarAlt,
} from "react-icons/fa";

const UserDashboard = () => {
  return (
    <Container fluid className="py-4 px-4">
      <h2 className="mb-4 fw-bold">
        User Dashboard
      </h2>

      {/* Stats */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-3">
            <div className="d-flex align-items-center">
              <FaMapMarkedAlt size={40} />

              <div className="ms-3">
                <h5>Total Tours</h5>
                <h3>18</h3>
              </div>
            </div>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-3">
            <div className="d-flex align-items-center">
              <FaHeart size={40} />

              <div className="ms-3">
                <h5>Favorites</h5>
                <h3>9</h3>
              </div>
            </div>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-3">
            <div className="d-flex align-items-center">
              <FaTaxi size={40} />

              <div className="ms-3">
                <h5>Cab Bookings</h5>
                <h3>5</h3>
              </div>
            </div>
          </Card>
        </Col>

        <Col md={3}>
          <Card className="shadow border-0 rounded-4 p-3">
            <div className="d-flex align-items-center">
              <FaCalendarAlt size={40} />

              <div className="ms-3">
                <h5>Upcoming Trips</h5>
                <h3>3</h3>
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      {/* Recent Bookings */}
      <Card className="shadow border-0 rounded-4">
        <Card.Body>
          <h4 className="mb-4">
            Recent Bookings
          </h4>

          <Table responsive hover>
            <thead>
              <tr>
                <th>Destination</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              <tr>
                <td>Goa Beach</td>
                <td>12 May 2026</td>
                <td>
                  <Badge bg="success">
                    Confirmed
                  </Badge>
                </td>
              </tr>

              <tr>
                <td>Manali Hills</td>
                <td>20 May 2026</td>
                <td>
                  <Badge bg="warning">
                    Pending
                  </Badge>
                </td>
              </tr>
            </tbody>
          </Table>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default UserDashboard;