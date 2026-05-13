import { useState } from "react";

import {
  Container,
  Form,
  Button,
  Card,
} from "react-bootstrap";

import axiosInstance from "../../api/axiosInstance";

import { useNavigate } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate();

  const [formData, setFormData] =
    useState({
      name: "",
      email: "",
      password: "",
    });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axiosInstance.post(
        "register/",
        formData
      );

      navigate("/login");
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Container className="py-5">
      <Card className="p-4 shadow-lg border-0 rounded-4 mx-auto"
        style={{ maxWidth: "500px" }}
      >
        <h2 className="text-center mb-4">
          Register
        </h2>

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>

            <Form.Control
              type="text"
              name="name"
              onChange={handleChange}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>

            <Form.Control
              type="email"
              name="email"
              onChange={handleChange}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>

            <Form.Control
              type="password"
              name="password"
              onChange={handleChange}
            />
          </Form.Group>

          <Button
            variant="dark"
            type="submit"
            className="w-100"
          >
            Register
          </Button>
        </Form>
      </Card>
    </Container>
  );
};

export default Register;