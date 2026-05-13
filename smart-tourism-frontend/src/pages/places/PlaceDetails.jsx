import { useEffect, useState } from "react";

import { useParams } from "react-router-dom";

import axiosInstance from "../../api/axiosInstance";

import {
  Container,
  Row,
  Col,
  Button,
  Card,
} from "react-bootstrap";

const PlaceDetails = () => {
  const { id } = useParams();

  const [place, setPlace] = useState(null);

  useEffect(() => {
    fetchPlace();
  }, []);

  const fetchPlace = async () => {
    try {
      const response = await axiosInstance.get(
        `places/${id}/`
      );

      setPlace(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  if (!place) {
    return <h2>Loading...</h2>;
  }

  return (
    <Container className="py-5">
      <Row>
        <Col md={6}>
          <img
            src={place.image}
            alt={place.name}
            className="img-fluid rounded-4 shadow"
          />
        </Col>

        <Col md={6}>
          <h1>{place.name}</h1>

          <p>{place.description}</p>

          <h5>Location: {place.location}</h5>

          <h5>Rating: ⭐ 4.8</h5>

          <Button variant="success">
            Book Tour
          </Button>
        </Col>
      </Row>

      {/* Reviews */}
      <div className="mt-5">
        <h3>User Reviews</h3>

        <Card className="mb-3">
          <Card.Body>
            Amazing tourist destination!
          </Card.Body>
        </Card>
      </div>
    </Container>
  );
};

export default PlaceDetails;