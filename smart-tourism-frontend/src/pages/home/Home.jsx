import {
  Container,
  Button,
  Row,
  Col,
  Card,
} from "react-bootstrap";

import { motion } from "framer-motion";

const Home = () => {

  return (

    <div className="hero-section py-5">

      <Container className="text-center text-light">

        {/* Hero Heading */}
        <motion.h1
          initial={{
            opacity: 0,
            y: -50,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 1,
          }}
          className="display-3 fw-bold"
        >

          Explore Beautiful Destinations

        </motion.h1>

        {/* Hero Subtitle */}
        <motion.p
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          transition={{
            delay: 0.5,
          }}
          className="lead mt-3"
        >

          Smart Tourism Management System

        </motion.p>

        {/* Explore Button */}
        <Button
          variant="warning"
          size="lg"
          className="mt-3 px-4 rounded-4"
        >
          Explore Now
        </Button>

        {/* Cards Section */}
        <Row className="mt-5 justify-content-center">

          {/* Weather Card */}
          <Col md={4} className="mb-4">

            <Card className="shadow border-0 rounded-4 p-4 text-dark">

              <h4>Live Weather</h4>

              <h2>28°C</h2>

              <p>Sunny • Hyderabad</p>

            </Card>

          </Col>

          {/* Destination Card */}
          <Col md={4} className="mb-4">

            <Card className="shadow border-0 rounded-4 p-4 text-dark">

              <h4>Top Destination</h4>

              <h2>Puri Beach</h2>

              <p>Odisha Tourism</p>

            </Card>

          </Col>

          {/* AI Assistant Card */}
          <Col md={4} className="mb-4">

            <Card className="shadow border-0 rounded-4 p-4 text-dark">

              <h4>AI Travel Assistant</h4>

              <h2>24/7 Support</h2>

              <p>Smart Recommendations</p>

            </Card>

          </Col>

        </Row>

      </Container>

    </div>
  );
};

export default Home;