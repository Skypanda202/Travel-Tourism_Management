import { Button, Col, Container, Form, Row } from "react-bootstrap";
import { motion } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";
import {
  FaMapMarkedAlt,
  FaRobot,
  FaRoute,
  FaSearch,
  FaStar,
} from "react-icons/fa";

const Home = () => {
  const navigate = useNavigate();

  const handleSearch = (event) => {
    event.preventDefault();
    const query = new FormData(event.currentTarget).get("search")?.trim();
    navigate(query ? `/places?search=${encodeURIComponent(query)}` : "/places");
  };

  return (
    <>
      <section className="hero-section">
        <Container>
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="hero-content"
          >
            <span className="hero-eyebrow">Tour and Travel Planner</span>

            <h1 className="hero-title">Discover places worth slowing down for</h1>

            <p className="hero-copy">
              Find destinations, check useful trip details, save favorites, and
              plan local travel with a simple visitor account.
            </p>

            <Form onSubmit={handleSearch} className="hero-search">
              <Row className="g-2 align-items-center">
                <Col lg>
                  <Form.Control
                    name="search"
                    type="search"
                    placeholder="Search waterfalls, temples, forests..."
                    aria-label="Search tourist places"
                  />
                </Col>

                <Col lg="auto">
                  <Button type="submit" className="btn-primary-soft w-100 px-4">
                    <FaSearch className="me-2" />
                    Search
                  </Button>
                </Col>
              </Row>
            </Form>

            <Row className="g-4 mt-4">
              <Col xs={4} className="hero-stat">
                <strong>Explore</strong>
                Places
              </Col>
              <Col xs={4} className="hero-stat">
                <strong>Plan</strong>
                Trips
              </Col>
              <Col xs={4} className="hero-stat">
                <strong>Ask</strong>
                Assistant
              </Col>
            </Row>
          </motion.div>
        </Container>
      </section>

      <section className="section-band">
        <Container>
          <Row className="align-items-end mb-4 g-3">
            <Col lg={8}>
              <span className="section-eyebrow">Plan with less guesswork</span>
              <h2 className="section-title">Everything for a smoother visit</h2>
              <p className="section-copy">
                Explore destinations, compare essentials, and move from idea to
                itinerary without jumping through different tools.
              </p>
            </Col>

            <Col lg={4} className="text-lg-end">
              <Button as={Link} to="/places" className="btn-primary-soft">
                Browse places
              </Button>
            </Col>
          </Row>

          <Row className="g-4">
            <Col md={4}>
              <div className="feature-card">
                <span className="feature-icon mb-3">
                  <FaMapMarkedAlt />
                </span>
                <h3 className="h5 fw-bold">Map-first exploring</h3>
                <p className="section-copy mb-0">
                  See where attractions sit before deciding what belongs in a
                  day plan.
                </p>
              </div>
            </Col>

            <Col md={4}>
              <div className="feature-card">
                <span className="feature-icon mb-3">
                  <FaRoute />
                </span>
                <h3 className="h5 fw-bold">Trip-ready details</h3>
                <p className="section-copy mb-0">
                  Ratings, fees, location notes, and descriptions are easy to
                  scan from each place card.
                </p>
              </div>
            </Col>

            <Col md={4}>
              <div className="feature-card">
                <span className="feature-icon mb-3">
                  <FaRobot />
                </span>
                <h3 className="h5 fw-bold">Assistant support</h3>
                <p className="section-copy mb-0">
                  Use the AI assistant for quick questions while you compare
                  routes and places.
                </p>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      <section className="section-band pt-0">
        <Container>
          <div className="detail-panel">
            <Row className="align-items-center g-4">
              <Col lg={8}>
                <span className="section-eyebrow">Popular starting point</span>
                <h2 className="section-title h1">Start with highly rated places</h2>
                <p className="section-copy">
                  Open the places page to search by name or city, then tap into
                  a destination for photos, entry information, and booking
                  actions.
                </p>
              </Col>

              <Col lg={4} className="text-lg-end">
                <Button as={Link} to="/places" className="btn-outline-soft me-2 mb-2">
                  <FaStar className="me-2" />
                  Top places
                </Button>
                <Button as={Link} to="/maps" className="btn-primary-soft mb-2">
                  Open map
                </Button>
              </Col>
            </Row>
          </div>
        </Container>
      </section>
    </>
  );
};

export default Home;
