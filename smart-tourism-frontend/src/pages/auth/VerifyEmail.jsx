import { useEffect, useState } from "react";
import { Alert, Button, Container, Spinner } from "react-bootstrap";
import { Link, useSearchParams } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";

const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState("loading");
  const [message, setMessage] = useState("Verifying your email...");

  useEffect(() => {
    const verify = async () => {
      const token = searchParams.get("token");
      if (!token) {
        setStatus("error");
        setMessage("Verification token is missing.");
        return;
      }

      try {
        const response = await axiosInstance.post("verify-email/", { token });
        setStatus("success");
        setMessage(response.data.message || "Email verified successfully.");
      } catch (error) {
        console.log(error);
        setStatus("error");
        setMessage(error.response?.data?.message || "Verification link is invalid or expired.");
      }
    };

    verify();
  }, [searchParams]);

  return (
    <section className="auth-page">
      <Container>
        <div className="auth-card text-center">
          {status === "loading" ? <Spinner animation="border" className="mb-3" /> : null}
          <span className="section-eyebrow">Email verification</span>
          <h1 className="h2 fw-bold mt-2 mb-3">
            {status === "success" ? "Verified" : "Account check"}
          </h1>
          <Alert variant={status === "success" ? "success" : status === "error" ? "danger" : "info"}>
            {message}
          </Alert>
          <Button as={Link} to="/login" className="btn-primary-soft mt-2">
            Go to login
          </Button>
        </div>
      </Container>
    </section>
  );
};

export default VerifyEmail;
