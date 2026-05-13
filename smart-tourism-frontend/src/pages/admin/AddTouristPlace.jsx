import {
  Container,
  Card,
  Form,
  Button,
  Spinner,
} from "react-bootstrap";

import { useState } from "react";

import axiosInstance from "../../api/axiosInstance";

import { toast } from "react-toastify";

const AddTouristPlace = () => {

  const [loading, setLoading] =
    useState(false);

  const [preview, setPreview] =
    useState(null);

  const [formData, setFormData] =
    useState({
      name: "",
      description: "",
      location: "",
      image: null,
    });

  // Handle Input Change
  const handleChange = (e) => {

    const { name, value, files } =
      e.target;

    // Image Upload
    if (name === "image") {

      const file = files[0];

      setFormData({
        ...formData,
        image: file,
      });

      // Image Preview
      setPreview(
        URL.createObjectURL(file)
      );

    } else {

      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  // Submit Form
  const handleSubmit = async (e) => {

    e.preventDefault();

    setLoading(true);

    const data = new FormData();

    data.append("name", formData.name);

    data.append(
      "description",
      formData.description
    );

    data.append(
      "location",
      formData.location
    );

    data.append(
      "image",
      formData.image
    );

    try {

      await axiosInstance.post(
        "admin/places/",
        data,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      toast.success(
        "Tourist Place Added Successfully!"
      );

      // Reset Form
      setFormData({
        name: "",
        description: "",
        location: "",
        image: null,
      });

      setPreview(null);

    } catch (error) {

      console.log(error);

      toast.error(
        "Failed to add tourist place"
      );

    } finally {

      setLoading(false);
    }
  };

  return (
    <Container className="py-5">

      <Card className="shadow-lg border-0 rounded-4 p-4">

        <h2 className="mb-4 text-center">
          Add Tourist Place
        </h2>

        <Form onSubmit={handleSubmit}>

          {/* Place Name */}
          <Form.Group className="mb-3">

            <Form.Label>
              Place Name
            </Form.Label>

            <Form.Control
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter place name"
              required
            />

          </Form.Group>

          {/* Description */}
          <Form.Group className="mb-3">

            <Form.Label>
              Description
            </Form.Label>

            <Form.Control
              as="textarea"
              rows={4}
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter description"
              required
            />

          </Form.Group>

          {/* Location */}
          <Form.Group className="mb-3">

            <Form.Label>
              Location
            </Form.Label>

            <Form.Control
              type="text"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="Enter location"
              required
            />

          </Form.Group>

          {/* Image Upload */}
          <Form.Group className="mb-4">

            <Form.Label>
              Upload Image
            </Form.Label>

            <Form.Control
              type="file"
              name="image"
              accept="image/*"
              onChange={handleChange}
              required
            />

          </Form.Group>

          {/* Image Preview */}
          {preview && (
            <div className="mb-4 text-center">

              <img
                src={preview}
                alt="preview"
                className="img-fluid rounded-4 shadow"
                style={{
                  maxHeight: "300px",
                  objectFit: "cover",
                }}
              />

            </div>
          )}

          {/* Submit Button */}
          <Button
            variant="dark"
            type="submit"
            className="w-100 rounded-3"
            disabled={loading}
          >

            {loading ? (
              <>
                <Spinner
                  animation="border"
                  size="sm"
                  className="me-2"
                />
                Uploading...
              </>
            ) : (
              "Add Place"
            )}

          </Button>

        </Form>

      </Card>

    </Container>
  );
};

export default AddTouristPlace;