import { useEffect, useState } from "react";
import { Alert, Badge, Button, Spinner, Table } from "react-bootstrap";
import { toast } from "react-toastify";
import axiosInstance from "../../api/axiosInstance";

const getList = (payload) => payload.results || payload.data || payload || [];

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        setError("");
        const response = await axiosInstance.get("users/");
        setUsers(getList(response.data));
      } catch (fetchError) {
        console.log(fetchError);
        setError("Could not load users. Check your admin login and API server.");
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const deleteUser = async (user) => {
    const confirmed = window.confirm(`Deactivate ${user.email}?`);
    if (!confirmed) {
      return;
    }

    try {
      await axiosInstance.delete(`users/${user.id}/`);
      setUsers((current) => current.map((item) => (
        item.id === user.id ? { ...item, is_active: false } : item
      )));
      toast.success("User deactivated");
    } catch (deleteError) {
      console.log(deleteError);
      toast.error("Could not deactivate user");
    }
  };

  if (loading) {
    return (
      <div className="loading-wrap">
        <Spinner animation="border" role="status" />
      </div>
    );
  }

  return (
    <div className="detail-panel">
      <span className="section-eyebrow">Admin accounts</span>
      <h1 className="h2 fw-bold mt-2 mb-4">User management</h1>

      {error ? <Alert variant="warning">{error}</Alert> : null}

      <div className="table-responsive">
        <Table hover className="align-middle">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th className="text-end">Action</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.full_name || user.username}</td>
                <td>{user.email}</td>
                <td className="text-capitalize">{user.role}</td>
                <td>
                  <Badge bg={user.is_active ? "success" : "secondary"}>
                    {user.is_active ? "Active" : "Inactive"}
                  </Badge>
                </td>
                <td className="text-end">
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => deleteUser(user)}
                    disabled={!user.is_active}
                  >
                    Delete account
                  </Button>
                </td>
              </tr>
            ))}
            {!users.length ? (
              <tr>
                <td colSpan="5" className="text-center section-copy py-4">
                  No users found.
                </td>
              </tr>
            ) : null}
          </tbody>
        </Table>
      </div>
    </div>
  );
};

export default UserManagement;
