import { useContext } from "react";
import { Button, Container, Form } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm } from "react-hook-form";
import { toast } from "react-toastify";
import * as yup from "yup";
import axiosInstance from "../../api/axiosInstance";
import AuthContext from "../../context/authContextValue";

const schema = yup.object({
  email: yup.string().email("Enter a valid email").required("Email is required"),
  password: yup.string().min(6, "Minimum 6 characters").required("Password is required"),
});

const Login = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data) => {
    try {
      const response = await axiosInstance.post("login/", {
        email: data.email,
        password: data.password,
      });

      const accessToken = response.data.access || response.data.access_token;
      const decodedUser = login(accessToken);
      const isAdmin = decodedUser.is_admin || decodedUser.role === "admin";

      toast.success("Login successful");
      navigate(isAdmin ? "/admin/places" : "/dashboard");
    } catch (error) {
      console.log(error);
      toast.error("Invalid email or password");
    }
  };

  return (
    <section className="auth-page">
      <Container>
        <div className="auth-card">
          <span className="section-eyebrow">Welcome back</span>
          <h1 className="h2 fw-bold mt-2 mb-2">Login to continue</h1>
          <p className="section-copy mb-4">
            Access saved places, bookings, and your travel dashboard.
          </p>

          <Form onSubmit={handleSubmit(onSubmit)} noValidate>
            <Form.Group className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="you@example.com"
                isInvalid={Boolean(errors.email)}
                {...register("email")}
              />
              <Form.Control.Feedback type="invalid">
                {errors.email?.message}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-4">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter password"
                isInvalid={Boolean(errors.password)}
                {...register("password")}
              />
              <Form.Control.Feedback type="invalid">
                {errors.password?.message}
              </Form.Control.Feedback>
            </Form.Group>

            <Button
              className="btn-primary-soft w-100"
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Logging in..." : "Login"}
            </Button>
          </Form>

          <p className="section-copy text-center mt-4 mb-0">
            New here? <Link to="/register">Create an account</Link>
          </p>
        </div>
      </Container>
    </section>
  );
};

export default Login;
