import AppRoutes from "./routes/AppRoutes";

// Toast Notifications
import {
  ToastContainer,
} from "react-toastify";

import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <>

      {/* Routes */}
      <AppRoutes />

      {/* Toast Notification */}
      <ToastContainer position="top-right" />

    </>
  );
}

export default App;