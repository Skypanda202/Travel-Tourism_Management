import AdminSidebar from "../components/admin/AdminSidebar";
import AdminTopbar from "../components/admin/AdminTopbar";

const AdminLayout = ({ children }) => {
  return (
    <div className="d-flex">
      <AdminSidebar />

      <div className="flex-grow-1">
        <AdminTopbar />

        <div className="p-4 bg-light min-vh-100">
          {children}
        </div>
      </div>
    </div>
  );
};

export default AdminLayout;