import { useContext, useRef, useState } from "react";
import { Button, Container, Form } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import axiosInstance from "../../api/axiosInstance";
import GoogleLoginButton from "../../components/auth/GoogleLoginButton";
import AuthContext from "../../context/authContextValue";
import { clearAuthSession, isAdminUser } from "../../utils/auth";

const Register = () => {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const submitInFlight = useRef(false);

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (submitInFlight.current) {
      return;
    }

    const payload = {
      ...formData,
      name: formData.name.trim(),
      email: formData.email.trim().toLowerCase(),
    };

    try {
      submitInFlight.current = true;
      setSubmitting(true);
      clearAuthSession();

      await axiosInstance.post("register/", payload);
      toast.success("Account created. Please check your email to verify it.");
      navigate("/login");
    } catch (error) {
      console.log(error);
      toast.error(
        error.response?.data?.error ||
          error.response?.data?.message ||
          error.response?.data?.detail ||
          "Registration failed"
      );
    } finally {
      submitInFlight.current = false;
      setSubmitting(false);
    }
  };

  const handleGoogleSuccess = (data) => {
    const accessToken = data.access || data.access_token;
    const decodedUser = login(accessToken, data.user);
    const isAdmin = isAdminUser(decodedUser);

    toast.success("Google account connected");
    navigate(isAdmin ? "/admin/places" : "/dashboard");
  };

  return (
    <section className="auth-page">
      <Container>
        <div className="auth-card">
          <span className="section-eyebrow">Create account</span>
          <h1 className="h2 fw-bold mt-2 mb-2">Start planning your trip</h1>
          <p className="section-copy mb-4">
            Save destinations and keep your travel activity in one place.
          </p>

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Your name"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="you@example.com"
                required
              />
            </Form.Group>

            <Form.Group className="mb-4">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Create password"
                minLength={6}
                required
              />
            </Form.Group>

            <Button
              className="btn-primary-soft w-100"
              type="submit"
              disabled={submitting}
            >
              {submitting ? "Creating account..." : "Create account"}
            </Button>
          </Form>

          <div className="my-3 text-center section-copy">or</div>
          <GoogleLoginButton
            label="Register with Google"
            onSuccess={handleGoogleSuccess}
          />

          <p className="section-copy text-center mt-4 mb-0">
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </div>
      </Container>
    </section>
  );
};

export default Register;
