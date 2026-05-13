import {
  Container,
  Card,
  Table,
  Button,
  Badge,
} from "react-bootstrap";

const CabManagement = () => {
  return (
    <Container fluid>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          Cab Booking Management
        </h3>

        <Table responsive hover>
          <thead>
            <tr>
              <th>User</th>
              <th>Cab</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Akash</td>

              <td>SUV Premium</td>

              <td>
                <Badge bg="warning">
                  Pending
                </Badge>
              </td>

              <td>
                <Button
                  variant="success"
                  size="sm"
                  className="me-2"
                >
                  Approve
                </Button>

                <Button
                  variant="danger"
                  size="sm"
                >
                  Reject
                </Button>
              </td>
            </tr>
          </tbody>
        </Table>
      </Card>
    </Container>
  );
};

export default CabManagement;