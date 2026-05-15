import AppRoutes from "./routes/AppRoutes";

import AuthProvider from "./context/AuthContext";

// Toast Notifications
import {
  ToastContainer,
} from "react-toastify";

import "react-toastify/dist/ReactToastify.css";

// Floating AI Chat
// import FloatingAIChat from "./components/chatbot/FloatingAIChat";

function App() {

  return (

    <AuthProvider>

      {/* Application Routes */}
      <AppRoutes />

      {/* Global Floating AI Assistant */}
      {/* <FloatingAIChat /> */}

      {/* Toast Notifications */}
      <ToastContainer
        position="top-right"
        autoClose={3000}
      />

    </AuthProvider>

  );
}

export default App;