import {
  Container,
  Card,
  Table,
  Button,
} from "react-bootstrap";

const ReviewsManagement = () => {
  return (
    <Container>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          Reviews Management
        </h3>

        <Table responsive hover>
          <thead>
            <tr>
              <th>User</th>
              <th>Place</th>
              <th>Review</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Akash</td>
              <td>Goa</td>
              <td>Beautiful destination!</td>

              <td>
                <Button
                  variant="danger"
                  size="sm"
                >
                  Delete
                </Button>
              </td>
            </tr>
          </tbody>
        </Table>
      </Card>
    </Container>
  );
};

export default ReviewsManagement;