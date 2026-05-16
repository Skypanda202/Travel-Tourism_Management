import { useEffect, useState } from "react";
import { Alert, Badge, Button, Col, Form, Row, Spinner, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import axiosInstance from "../../api/axiosInstance";

const defaultCategories = [
  { name: "Cafes", icon: "coffee", description: "Local cafes and food stops" },
  { name: "Lodges", icon: "bed", description: "Lodges and visitor stays" },
];

const getList = (payload) => payload.results || payload.data || payload || [];

const ManagePlaces = () => {
  const [places, setPlaces] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categoryName, setCategoryName] = useState("");
  const [error, setError] = useState("");

  const fetchData = async () => {
    try {
      setLoading(true);
      setError("");
      const [placesResponse, categoriesResponse] = await Promise.all([
        axiosInstance.get("places/"),
        axiosInstance.get("places/categories/"),
      ]);
      setPlaces(getList(placesResponse.data));
      setCategories(getList(categoriesResponse.data));
    } catch (fetchError) {
      console.log(fetchError);
      setError("Could not load places. Check your admin login and API server.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    Promise.resolve().then(fetchData);
  }, []);

  const handleDelete = async (place) => {
    const confirmed = window.confirm(`Delete ${place.name}? This removes it from public listings.`);
    if (!confirmed) {
      return;
    }

    try {
      await axiosInstance.delete(`places/${place.slug}/`);
      setPlaces((current) => current.filter((item) => item.slug !== place.slug));
      toast.success("Place deleted");
    } catch (deleteError) {
      console.log(deleteError);
      toast.error("Could not delete this place");
    }
  };

  const createCategory = async (category) => {
    try {
      const response = await axiosInstance.post("places/categories/", {
        ...category,
        name: category.name || categoryName,
        is_active: true,
      });
      setCategories((current) => [...current, response.data.data || response.data]);
      setCategoryName("");
      toast.success("Category added");
    } catch (categoryError) {
      console.log(categoryError);
      toast.error(categoryError.response?.data?.name?.[0] || "Could not add category");
    }
  };

  if (loading) {
    return (
      <div className="loading-wrap">
        <Spinner animation="border" role="status" />
      </div>
    );
  }

  return (
    <div className="detail-panel">
      <Row className="align-items-end mb-4 g-3">
        <Col lg={7}>
          <span className="section-eyebrow">Admin inventory</span>
          <h1 className="h2 fw-bold mt-2 mb-2">Manage places</h1>
          <p className="section-copy mb-0">
            Add, edit, delete, and organize tourist places, cafes, and lodges.
          </p>
        </Col>
        <Col lg={5} className="text-lg-end">
          <Button as={Link} to="/admin/places/add" className="btn-primary-soft">
            Add place
          </Button>
        </Col>
      </Row>

      {error ? <Alert variant="warning">{error}</Alert> : null}

      <div className="search-panel mb-4">
        <Row className="g-3 align-items-end">
          <Col lg={5}>
            <Form.Group>
              <Form.Label>Add category</Form.Label>
              <Form.Control
                value={categoryName}
                onChange={(event) => setCategoryName(event.target.value)}
                placeholder="Cafe, Lodge, Eco stay..."
              />
            </Form.Group>
          </Col>
          <Col lg={7}>
            <div className="d-flex flex-wrap gap-2">
              <Button
                type="button"
                className="btn-outline-soft"
                onClick={() => categoryName.trim() && createCategory({ name: categoryName.trim() })}
              >
                Add custom category
              </Button>
              {defaultCategories.map((category) => (
                <Button
                  type="button"
                  className="btn-outline-soft"
                  key={category.name}
                  onClick={() => createCategory(category)}
                  disabled={categories.some((item) => item.name.toLowerCase() === category.name.toLowerCase())}
                >
                  Add {category.name}
                </Button>
              ))}
            </div>
          </Col>
        </Row>
      </div>

      <div className="table-responsive">
        <Table hover className="align-middle">
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Location</th>
              <th>Status</th>
              <th className="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            {places.map((place) => (
              <tr key={place.id || place.slug}>
                <td className="fw-semibold">{place.name}</td>
                <td>{place.category_name || place.category?.name || "Uncategorized"}</td>
                <td>{[place.city, place.country].filter(Boolean).join(", ")}</td>
                <td>
                  <Badge bg={place.status === "published" || !place.status ? "success" : "secondary"}>
                    {place.status || "published"}
                  </Badge>
                </td>
                <td className="text-end">
                  <Button
                    as={Link}
                    to={`/admin/places/${place.slug}/edit`}
                    className="btn-outline-soft btn-sm me-2"
                  >
                    Edit
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleDelete(place)}
                  >
                    Delete
                  </Button>
                </td>
              </tr>
            ))}
            {!places.length ? (
              <tr>
                <td colSpan="5" className="text-center section-copy py-4">
                  No places found. Add the first destination to begin.
                </td>
              </tr>
            ) : null}
          </tbody>
        </Table>
      </div>
    </div>
  );
};

export default ManagePlaces;
