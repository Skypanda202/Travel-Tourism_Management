import { useEffect, useState } from "react";
import axiosInstance from "../../api/axiosInstance";

import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Form,
} from "react-bootstrap";

import { Link } from "react-router-dom";

import { motion } from "framer-motion";

const TouristPlaces = () => {
  const [places, setPlaces] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchPlaces();
  }, []);

  const fetchPlaces = async () => {
    try {
      const response = await axiosInstance.get(
        "places/"
      );

      setPlaces(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const filteredPlaces = places.filter((place) =>
    place.name
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <Container className="py-5">
      <h1 className="mb-4 text-center">
        Tourist Places
      </h1>

      {/* Search */}
      <Form className="mb-5">
        <Form.Control
          type="text"
          placeholder="Search tourist places..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </Form>

      {/* Cards */}
      <Row>
        {filteredPlaces.map((place) => (
          <Col md={4} className="mb-4" key={place.id}>
            <motion.div
              whileHover={{ scale: 1.05 }}
            >
              <Card className="shadow-lg border-0 rounded-4">
                <Card.Img
                  variant="top"
                  src={place.image}
                  style={{
                    height: "250px",
                    objectFit: "cover",
                  }}
                />

                <Card.Body>
                  <Card.Title>
                    {place.name}
                  </Card.Title>

                  <Card.Text>
                    {place.description.slice(0, 100)}
                  </Card.Text>

                  <Link to={`/place/${place.id}`}>
                    <Button variant="dark">
                      View Details
                    </Button>
                  </Link>
                </Card.Body>
              </Card>
            </motion.div>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default TouristPlaces;