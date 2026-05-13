import {
  Container,
  Card,
  Table,
  Button,
} from "react-bootstrap";

const UserManagement = () => {
  return (
    <Container>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          User Management
        </h3>

        <Table responsive hover>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr>
              <td>Akash</td>
              <td>akash@gmail.com</td>
              <td>User</td>

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

export default UserManagement;