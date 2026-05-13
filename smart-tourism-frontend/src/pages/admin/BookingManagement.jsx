import {
  Container,
  Card,
  Table,
  Button,
} from "react-bootstrap";

const BookingManagement = () => {
  return (
    <Container>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          Booking Management
        </h3>

        <Table responsive hover>
          <thead>
            <tr>
              <th>User</th>
              <th>Place</th>
              <th>Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Akash</td>
              <td>Goa</td>
              <td>15 May</td>
              <td>Pending</td>

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

export default BookingManagement;