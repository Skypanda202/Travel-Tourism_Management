import { useEffect, useState } from "react";
import { Alert, Button, Col, Container, Form, Row, Spinner } from "react-bootstrap";
import { Link, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import {
  FaCalendarCheck,
  FaClock,
  FaHeart,
  FaLocationArrow,
  FaMapMarkerAlt,
  FaRupeeSign,
  FaStar,
} from "react-icons/fa";
import axiosInstance from "../../api/axiosInstance";

const fallbackImage =
  "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1400&q=80";

const unwrapPlace = (data) => data?.data || data;

const calculateDistanceKm = (start, end) => {
  const radius = 6371;
  const toRadians = (value) => (value * Math.PI) / 180;
  const dLat = toRadians(end.lat - start.lat);
  const dLon = toRadians(end.lng - start.lng);
  const lat1 = toRadians(start.lat);
  const lat2 = toRadians(end.lat);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  return radius * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
};

const PlaceDetails = () => {
  const { id } = useParams();
  const [place, setPlace] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [reviewForm, setReviewForm] = useState({
    rating: "5",
    title: "",
    content: "",
  });
  const [bookingUrl, setBookingUrl] = useState("");
  const [distanceKm, setDistanceKm] = useState(null);
  const [locationLoading, setLocationLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPlace = async () => {
      try {
        setLoading(true);
        setError("");
        const response = await axiosInstance.get(`places/${id}/`);
        const nextPlace = unwrapPlace(response.data);
        setPlace(nextPlace);

        const reviewsResponse = await axiosInstance.get(`reviews/?place=${nextPlace.id}`);
        setReviews(reviewsResponse.data.results || reviewsResponse.data.data || []);
      } catch (fetchError) {
        console.log(fetchError);
        setError("This place could not be loaded. Please return to the places page.");
      } finally {
        setLoading(false);
      }
    };

    fetchPlace();
  }, [id]);

  const handleFavorite = async () => {
    if (!localStorage.getItem("token")) {
      toast.info("Please login as a visitor to save favorites.");
      return;
    }

    try {
      const response = await axiosInstance.post(`places/${place.slug}/favorite/`);
      const isFavorited = response.data.data?.is_favorited;
      setPlace((current) => ({
        ...current,
        is_favorited: isFavorited,
      }));
      toast.success(isFavorited ? "Added to favorites" : "Removed from favorites");
    } catch (favoriteError) {
      console.log(favoriteError);
      toast.error("Could not update favorite.");
    }
  };

  const handleReviewSubmit = async (event) => {
    event.preventDefault();

    if (!localStorage.getItem("token")) {
      toast.info("Please login as a visitor to add a review.");
      return;
    }

    try {
      await axiosInstance.post("reviews/", {
        place: place.id,
        rating: Number(reviewForm.rating),
        cleanliness_rating: Number(reviewForm.rating),
        accessibility_rating: Number(reviewForm.rating),
        value_rating: Number(reviewForm.rating),
        title: reviewForm.title,
        content: reviewForm.content,
      });

      toast.success("Review submitted for approval.");
      setReviewForm({ rating: "5", title: "", content: "" });
    } catch (reviewError) {
      console.log(reviewError);
      const message =
        reviewError.response?.data?.error?.message ||
        reviewError.response?.data?.message ||
        "Could not submit review.";
      toast.error(message);
    }
  };

  const handleLiveBooking = () => {
    if (!navigator.geolocation) {
      toast.error("Live location is not supported in this browser.");
      return;
    }

    setLocationLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const start = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        const end = {
          lat: Number(place.latitude),
          lng: Number(place.longitude),
        };
        const distance = calculateDistanceKm(start, end);
        setDistanceKm(distance);
        setBookingUrl(
          `/cab-booking?pickup_lat=${start.lat.toFixed(6)}&pickup_lng=${start.lng.toFixed(6)}&dropoff=${encodeURIComponent(
            place.name
          )}&dropoff_lat=${end.lat.toFixed(6)}&dropoff_lng=${end.lng.toFixed(6)}&distance=${distance.toFixed(2)}`
        );
        setLocationLoading(false);
        toast.success("Live location added for cab booking.");
      },
      () => {
        setLocationLoading(false);
        toast.error("Allow location access to book from your current location.");
      }
    );
  };

  if (loading) {
    return (
      <div className="loading-wrap">
        <Spinner animation="border" role="status" />
      </div>
    );
  }

  if (error || !place) {
    return (
      <section className="section-band">
        <Container>
          <Alert variant="warning">{error || "Place not found."}</Alert>
          <Button as={Link} to="/places" className="btn-primary-soft">
            Back to places
          </Button>
        </Container>
      </section>
    );
  }

  const image = place.cover_image_url || place.image || fallbackImage;
  const location = [place.address, place.city, place.state || place.country]
    .filter(Boolean)
    .join(", ");

  return (
    <section className="section-band">
      <Container>
        <Row className="g-5 align-items-start">
          <Col lg={7}>
            <img src={image} alt={place.name} className="detail-image" />
          </Col>

          <Col lg={5}>
            <div className="detail-panel">
              <span className="section-eyebrow">
                {place.category?.name || place.category_name || "Destination"}
              </span>

              <h1 className="section-title">{place.name}</h1>

              <p className="section-copy mb-4">
                {place.description || place.short_desc || "Details will be updated soon."}
              </p>

              <div className="d-grid gap-3 mb-4">
                <div className="d-flex gap-3">
                  <FaMapMarkerAlt className="mt-1 text-success" />
                  <span>{location || "Location details available soon"}</span>
                </div>

                <div className="d-flex gap-3">
                  <FaStar className="mt-1 text-warning" />
                  <span>
                    {place.avg_rating
                      ? `${Number(place.avg_rating).toFixed(1)} rating`
                      : "Ratings coming soon"}
                  </span>
                </div>

                <div className="d-flex gap-3">
                  <FaRupeeSign className="mt-1 text-success" />
                  <span>
                    {place.is_free
                      ? "Free entry"
                      : `${place.entry_fee || "Entry fee"} ${place.entry_fee_currency || ""}`}
                  </span>
                </div>

                <div className="d-flex gap-3">
                  <FaClock className="mt-1 text-success" />
                  <span>
                    {place.opening_time && place.closing_time
                      ? `${place.opening_time} to ${place.closing_time}${
                          place.open_days ? `, ${place.open_days}` : ""
                        }`
                      : "Opening hours not listed"}
                  </span>
                </div>
              </div>

              <div className="d-flex flex-wrap gap-2">
                <Button type="button" className="btn-outline-soft" onClick={handleFavorite}>
                  <FaHeart className="me-2" />
                  {place.is_favorited ? "Saved" : "Add favorite"}
                </Button>

                <Button
                  type="button"
                  className="btn-outline-soft"
                  onClick={handleLiveBooking}
                  disabled={locationLoading}
                >
                  <FaLocationArrow className="me-2" />
                  {locationLoading ? "Getting location..." : "Use live location"}
                </Button>

                <Button
                  as={Link}
                  to={bookingUrl || "/cab-booking"}
                  className="btn-primary-soft"
                >
                  <FaCalendarCheck className="me-2" />
                  Book travel
                </Button>
              </div>

              {distanceKm ? (
                <p className="section-copy mt-3 mb-0">
                  Nearby estimate: {distanceKm.toFixed(2)} km from your current location.
                </p>
              ) : null}
            </div>
          </Col>
        </Row>

        <Row className="g-4 mt-4">
          <Col lg={6}>
            <div className="detail-panel h-100">
              <h2 className="h4 fw-bold">Add review</h2>
              <Form onSubmit={handleReviewSubmit}>
                <Row className="g-3">
                  <Col md={4}>
                    <Form.Group>
                      <Form.Label>Rating</Form.Label>
                      <Form.Select
                        value={reviewForm.rating}
                        onChange={(event) =>
                          setReviewForm((current) => ({
                            ...current,
                            rating: event.target.value,
                          }))
                        }
                      >
                        {[5, 4, 3, 2, 1].map((rating) => (
                          <option value={rating} key={rating}>
                            {rating}
                          </option>
                        ))}
                      </Form.Select>
                    </Form.Group>
                  </Col>
                  <Col md={8}>
                    <Form.Group>
                      <Form.Label>Title</Form.Label>
                      <Form.Control
                        value={reviewForm.title}
                        onChange={(event) =>
                          setReviewForm((current) => ({
                            ...current,
                            title: event.target.value,
                          }))
                        }
                        required
                      />
                    </Form.Group>
                  </Col>
                  <Col md={12}>
                    <Form.Group>
                      <Form.Label>Review</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={4}
                        value={reviewForm.content}
                        onChange={(event) =>
                          setReviewForm((current) => ({
                            ...current,
                            content: event.target.value,
                          }))
                        }
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>
                <Button type="submit" className="btn-primary-soft mt-3">
                  Submit review
                </Button>
              </Form>
            </div>
          </Col>

          <Col lg={6}>
            <div className="detail-panel h-100">
              <h2 className="h4 fw-bold">Visitor reviews</h2>
              {reviews.length ? (
                <div className="d-grid gap-3">
                  {reviews.map((review) => (
                    <div className="feature-card shadow-none" key={review.id}>
                      <div className="d-flex justify-content-between gap-3">
                        <strong>{review.title}</strong>
                        <span>{review.rating}/5</span>
                      </div>
                      <p className="section-copy mb-1">{review.content}</p>
                      <small className="text-secondary">{review.user_name}</small>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="section-copy mb-0">No approved reviews yet.</p>
              )}
            </div>
          </Col>
        </Row>
      </Container>
    </section>
  );
};

export default PlaceDetails;
