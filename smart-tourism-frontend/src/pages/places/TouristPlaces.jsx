import { useEffect, useMemo, useState } from "react";
import { Alert, Button, Col, Container, Form, Row, Spinner } from "react-bootstrap";
import { useSearchParams } from "react-router-dom";
import { FaSearch, FaTimes } from "react-icons/fa";
import axiosInstance from "../../api/axiosInstance";
import PlaceCard from "../../components/cards/PlaceCard";

const getPlacesFromResponse = (data) => {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  if (Array.isArray(data?.data)) return data.data;
  return [];
};

const TouristPlaces = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [places, setPlaces] = useState([]);
  const [city, setCity] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const search = searchParams.get("search") || "";

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        setLoading(true);
        setError("");
        const response = await axiosInstance.get("places/");
        setPlaces(getPlacesFromResponse(response.data));
      } catch (fetchError) {
        console.log(fetchError);
        setError("Places could not be loaded. Please check the server and try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchPlaces();
  }, []);

  const cities = useMemo(() => {
    const uniqueCities = places
      .map((place) => place.city)
      .filter(Boolean)
      .sort((first, second) => first.localeCompare(second));

    return ["all", ...new Set(uniqueCities)];
  }, [places]);

  const filteredPlaces = places.filter((place) => {
    const searchText = `${place.name} ${place.city || ""} ${place.short_desc || ""}`
      .toLowerCase();
    const matchesSearch = searchText.includes(search.toLowerCase());
    const matchesCity = city === "all" || place.city === city;
    return matchesSearch && matchesCity;
  });

  const handleSearchChange = (event) => {
    const value = event.target.value;
    setSearchParams(value ? { search: value } : {});
  };

  const clearFilters = () => {
    setCity("all");
    setSearchParams({});
  };

  return (
    <section className="section-band">
      <Container>
        <Row className="align-items-end mb-4 g-3">
          <Col lg={7}>
            <span className="section-eyebrow">Explore destinations</span>
            <h1 className="section-title">Tourist places</h1>
            <p className="section-copy">
              Search destinations, narrow by city, and open the places that fit
              your travel plan.
            </p>
          </Col>

          <Col lg={5}>
            <div className="search-panel">
              <Row className="g-2">
                <Col md={7}>
                  <div className="position-relative">
                    <FaSearch className="position-absolute top-50 start-0 translate-middle-y ms-3 text-secondary" />
                    <Form.Control
                      type="search"
                      value={search}
                      onChange={handleSearchChange}
                      placeholder="Search places"
                      className="ps-5"
                      aria-label="Search places"
                    />
                  </div>
                </Col>

                <Col md={5}>
                  <Form.Select
                    value={city}
                    onChange={(event) => setCity(event.target.value)}
                    aria-label="Filter by city"
                  >
                    {cities.map((cityName) => (
                      <option value={cityName} key={cityName}>
                        {cityName === "all" ? "All cities" : cityName}
                      </option>
                    ))}
                  </Form.Select>
                </Col>
              </Row>
            </div>
          </Col>
        </Row>

        {error ? (
          <Alert variant="warning">{error}</Alert>
        ) : null}

        {loading ? (
          <div className="loading-wrap">
            <Spinner animation="border" role="status" />
          </div>
        ) : filteredPlaces.length ? (
          <Row className="g-4">
            {filteredPlaces.map((place) => (
              <Col md={6} lg={4} key={place.id || place.slug}>
                <PlaceCard place={place} />
              </Col>
            ))}
          </Row>
        ) : (
          <div className="empty-state">
            <h2 className="h4 text-dark">No places found</h2>
            <p className="mb-3">Try a different search term or remove filters.</p>
            <Button type="button" className="btn-outline-soft" onClick={clearFilters}>
              <FaTimes className="me-2" />
              Clear filters
            </Button>
          </div>
        )}
      </Container>
    </section>
  );
};

export default TouristPlaces;
