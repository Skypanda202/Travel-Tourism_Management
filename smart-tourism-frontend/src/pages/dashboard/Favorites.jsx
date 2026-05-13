import {
  Container,
  Row,
  Col,
  Card,
  Button,
} from "react-bootstrap";

const Favorites = () => {
  const favorites = [
    {
      id: 1,
      name: "Goa",
      image:
        "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86",
    },
    {
      id: 2,
      name: "Manali",
      image:
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
    },
  ];

  return (
    <Container className="py-5">
      <h2 className="mb-4">
        Favorite Places
      </h2>

      <Row>
        {favorites.map((place) => (
          <Col md={4} key={place.id}>
            <Card className="shadow border-0 rounded-4 mb-4">
              <Card.Img
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

                <Button variant="danger">
                  Remove
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default Favorites;