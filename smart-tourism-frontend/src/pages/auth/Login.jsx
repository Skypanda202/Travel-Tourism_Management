import React, {
  useContext,
} from "react";

import {
  Container,
  Form,
  Button,
  Card,
} from "react-bootstrap";

import axiosInstance from "../../api/axiosInstance";

import { AuthContext }
from "../../context/AuthContext";

import { useNavigate }
from "react-router-dom";

// React Hook Form
import { useForm }
from "react-hook-form";

import { yupResolver }
from "@hookform/resolvers/yup";

import * as yup from "yup";

// Toast
import { toast }
from "react-toastify";

// Validation Schema
const schema = yup.object({
  email: yup
    .string()
    .email("Enter valid email")
    .required("Email is required"),

  password: yup
    .string()
    .min(6, "Minimum 6 characters")
    .required("Password is required"),
});

const Login = () => {

  const { login } =
    useContext(AuthContext);

  const navigate = useNavigate();

  // React Hook Form
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });

  // Submit Function
  const onSubmit = async (data) => {

    try {

      const response =
        await axiosInstance.post(
          "login/",
          {
            email: data.email,
            password: data.password,
          }
        );

      // Save JWT token
      login(response.data.access);

      // Success Toast
      toast.success(
        "Login Successful!"
      );

      // Redirect
      navigate("/");

    } catch (error) {

      console.log(error);

      toast.error(
        "Invalid email or password"
      );
    }
  };

  return (
    <Container className="py-5">

      <Card
        className="p-4 shadow-lg border-0 rounded-4 mx-auto"
        style={{ maxWidth: "500px" }}
      >

        <h2 className="text-center mb-4">
          Login
        </h2>

        <Form
          onSubmit={handleSubmit(onSubmit)}
        >

          {/* Email */}
          <Form.Group className="mb-3">

            <Form.Label>
              Email
            </Form.Label>

            <Form.Control
              type="email"
              placeholder="Enter email"
              {...register("email")}
            />

            <p className="text-danger mt-1">
              {errors.email?.message}
            </p>

          </Form.Group>

          {/* Password */}
          <Form.Group className="mb-3">

            <Form.Label>
              Password
            </Form.Label>

            <Form.Control
              type="password"
              placeholder="Enter password"
              {...register("password")}
            />

            <p className="text-danger mt-1">
              {errors.password?.message}
            </p>

          </Form.Group>

          {/* Login Button */}
          <Button
            variant="dark"
            type="submit"
            className="w-100"
          >
            Login
          </Button>

        </Form>

      </Card>

    </Container>
  );
};

export default Login;