import {
  Container,
  Row,
  Col,
  Card,
  Button,
  Modal,
  Form,
} from "react-bootstrap";

import { useState } from "react";

const CabBooking = () => {
  const [show, setShow] = useState(false);

  const cabs = [
    {
      id: 1,
      name: "SUV Premium",
      price: "₹2500",
      image:
        "https://images.unsplash.com/photo-1502877338535-766e1452684a",
    },
    {
      id: 2,
      name: "Sedan Deluxe",
      price: "₹1800",
      image:
        "https://images.unsplash.com/photo-1494976388531-d1058494cdd8",
    },
  ];

  return (
    <Container className="py-5">
      <h2 className="mb-5 text-center">
        Cab Booking
      </h2>

      <Row>
        {cabs.map((cab) => (
          <Col md={4} key={cab.id}>
            <Card className="shadow border-0 rounded-4 mb-4">
              <Card.Img
                src={cab.image}
                style={{
                  height: "220px",
                  objectFit: "cover",
                }}
              />

              <Card.Body>
                <Card.Title>
                  {cab.name}
                </Card.Title>

                <h5>{cab.price}</h5>

                <Button
                  variant="dark"
                  onClick={() => setShow(true)}
                >
                  Book Now
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Modal */}
      <Modal
        show={show}
        onHide={() => setShow(false)}
      >
        <Modal.Header closeButton>
          <Modal.Title>
            Confirm Booking
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>
                Pickup Location
              </Form.Label>

              <Form.Control type="text" />
            </Form.Group>

            <Form.Group>
              <Form.Label>
                Destination
              </Form.Label>

              <Form.Control type="text" />
            </Form.Group>
          </Form>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="success">
            Confirm Booking
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default CabBooking;