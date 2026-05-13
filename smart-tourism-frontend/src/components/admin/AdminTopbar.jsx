const AdminTopbar = () => {
  return (
    <div className="bg-white shadow-sm p-3 d-flex justify-content-between align-items-center">
      <h4 className="fw-bold mb-0">
        Smart Tourism Admin
      </h4>

      <div className="d-flex align-items-center">
        <img
          src="https://i.pravatar.cc/40"
          alt="admin"
          className="rounded-circle"
        />

        <span className="ms-2 fw-semibold">
          Admin
        </span>
      </div>
    </div>
  );
};

export default AdminTopbar;