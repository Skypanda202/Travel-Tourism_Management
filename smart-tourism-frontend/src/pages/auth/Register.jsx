import { useState } from "react";
import { Button, Container, Form } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import axiosInstance from "../../api/axiosInstance";

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (event) => {
    setFormData({
      ...formData,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setSubmitting(true);
      await axiosInstance.post("register/", formData);
      toast.success("Account created. Please login.");
      navigate("/login");
    } catch (error) {
      console.log(error);
      toast.error(error.response?.data?.error || "Registration failed");
    } finally {
      setSubmitting(false);
    }
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

          <p className="section-copy text-center mt-4 mb-0">
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </div>
      </Container>
    </section>
  );
};

export default Register;
