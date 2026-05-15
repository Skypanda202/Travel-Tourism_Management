import { useEffect, useState } from "react";
import { Alert, Button, Col, Container, Row, Spinner } from "react-bootstrap";
import { Link } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import PlaceCard from "../../components/cards/PlaceCard";

const Favorites = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        setLoading(true);
        setError("");
        const response = await axiosInstance.get("users/favorites/");
        setFavorites(response.data.data || []);
      } catch (fetchError) {
        console.log(fetchError);
        setError("Could not load favorites. Please login again.");
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, []);

  return (
    <section className="section-band">
      <Container>
        <Row className="align-items-end mb-4 g-3">
          <Col lg={8}>
            <span className="section-eyebrow">Saved places</span>
            <h1 className="section-title">Favorites</h1>
            <p className="section-copy">
              Places you save from the destination pages will appear here.
            </p>
          </Col>
          <Col lg={4} className="text-lg-end">
            <Button as={Link} to="/places" className="btn-primary-soft">
              Browse places
            </Button>
          </Col>
        </Row>

        {error ? <Alert variant="warning">{error}</Alert> : null}

        {loading ? (
          <div className="loading-wrap">
            <Spinner animation="border" role="status" />
          </div>
        ) : favorites.length ? (
          <Row className="g-4">
            {favorites.map((favorite) => (
              <Col md={6} lg={4} key={favorite.id}>
                <PlaceCard place={favorite.place} />
              </Col>
            ))}
          </Row>
        ) : (
          <div className="empty-state">
            <h2 className="h4 text-dark">No favorites yet</h2>
            <p className="mb-3">Explore places and save the ones you like.</p>
            <Button as={Link} to="/places" className="btn-primary-soft">
              Explore places
            </Button>
          </div>
        )}
      </Container>
    </section>
  );
};

export default Favorites;
