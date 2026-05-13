import {
  Container,
  Card,
  Table,
  Button,
} from "react-bootstrap";

const ManagePlaces = () => {
  return (
    <Container fluid>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          Manage Tourist Places
        </h3>

        <Table responsive hover>
          <thead>
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Goa Beach</td>

              <td>Goa</td>

              <td>
                <Button
                  variant="primary"
                  size="sm"
                  className="me-2"
                >
                  Update
                </Button>

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

export default ManagePlaces;