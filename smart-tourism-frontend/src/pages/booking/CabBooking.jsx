import { useEffect, useMemo, useState } from "react";
import { Alert, Button, Col, Container, Form, Row, Spinner } from "react-bootstrap";
import { Link, useSearchParams } from "react-router-dom";
import { toast } from "react-toastify";
import { FaCalendarCheck, FaLocationArrow, FaMapMarkerAlt, FaRupeeSign } from "react-icons/fa";
import axiosInstance from "../../api/axiosInstance";

const fallbackCabImage =
  "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=900&q=80";

const unwrapList = (data) => data?.results || data?.data || data || [];

const defaultPickupTime = () => {
  const date = new Date(Date.now() + 60 * 60 * 1000);
  date.setMinutes(Math.ceil(date.getMinutes() / 15) * 15, 0, 0);
  return date.toISOString().slice(0, 16);
};

const formatMoney = (value) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(value || 0));

const CabBooking = () => {
  const [searchParams] = useSearchParams();
  const [cabTypes, setCabTypes] = useState([]);
  const [selectedCabId, setSelectedCabId] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [locationLoading, setLocationLoading] = useState(false);
  const [formData, setFormData] = useState({
    pickup_address: searchParams.get("pickup") || "My current location",
    pickup_latitude: searchParams.get("pickup_lat") || "",
    pickup_longitude: searchParams.get("pickup_lng") || "",
    dropoff_address: searchParams.get("dropoff") || "",
    dropoff_latitude: searchParams.get("dropoff_lat") || "",
    dropoff_longitude: searchParams.get("dropoff_lng") || "",
    distance_km: searchParams.get("distance") || "",
    pickup_datetime: defaultPickupTime(),
    num_passengers: "1",
    special_requests: "",
  });

  useEffect(() => {
    const fetchCabTypes = async () => {
      try {
        setLoading(true);
        const response = await axiosInstance.get("cabs/types/");
        const nextCabTypes = unwrapList(response.data);
        setCabTypes(nextCabTypes);
        setSelectedCabId(nextCabTypes[0]?.id ? String(nextCabTypes[0].id) : "");
      } catch (error) {
        console.log(error);
        toast.error("Cab options could not be loaded.");
      } finally {
        setLoading(false);
      }
    };

    fetchCabTypes();
  }, []);

  const selectedCab = useMemo(
    () => cabTypes.find((cab) => String(cab.id) === String(selectedCabId)),
    [cabTypes, selectedCabId]
  );

  const estimatedFare = useMemo(() => {
    if (!selectedCab || !formData.distance_km) {
      return null;
    }

    return Number(selectedCab.base_fare || 0) + Number(selectedCab.price_per_km || 0) * Number(formData.distance_km);
  }, [formData.distance_km, selectedCab]);

  const updateField = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleUseLiveLocation = () => {
    if (!navigator.geolocation) {
      toast.error("Live location is not supported in this browser.");
      return;
    }

    setLocationLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setFormData((current) => ({
          ...current,
          pickup_address: current.pickup_address || "My current location",
          pickup_latitude: position.coords.latitude.toFixed(6),
          pickup_longitude: position.coords.longitude.toFixed(6),
        }));
        setLocationLoading(false);
        toast.success("Pickup location updated.");
      },
      () => {
        setLocationLoading(false);
        toast.error("Allow location access to use live pickup.");
      }
    );
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!localStorage.getItem("token")) {
      toast.info("Please login as a visitor to book a cab.");
      return;
    }

    if (!selectedCabId) {
      toast.error("Please select a cab type.");
      return;
    }

    setSubmitting(true);
    try {
      const payload = {
        cab_type: Number(selectedCabId),
        pickup_address: formData.pickup_address,
        pickup_latitude: formData.pickup_latitude || null,
        pickup_longitude: formData.pickup_longitude || null,
        dropoff_address: formData.dropoff_address,
        dropoff_latitude: formData.dropoff_latitude || null,
        dropoff_longitude: formData.dropoff_longitude || null,
        distance_km: formData.distance_km || null,
        pickup_datetime: new Date(formData.pickup_datetime).toISOString(),
        num_passengers: Number(formData.num_passengers),
        special_requests: formData.special_requests,
      };

      const response = await axiosInstance.post("cabs/bookings/", payload);
      const booking = response.data?.data || response.data;
      toast.success(`Cab booking created${booking?.booking_ref ? `: ${booking.booking_ref}` : "."}`);
    } catch (error) {
      console.log(error);
      const message =
        error.response?.data?.error?.message ||
        error.response?.data?.message ||
        "Cab booking could not be created.";
      toast.error(message);
    } finally {
      setSubmitting(false);
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
    <section className="section-band">
      <Container>
        <div className="mb-4">
          <span className="section-eyebrow">Visitor cab booking</span>
          <h1 className="section-title">Book from your live location</h1>
          <p className="section-copy">
            Choose a cab, confirm your pickup, and send the request directly to the admin team.
          </p>
        </div>

        {!localStorage.getItem("token") ? (
          <Alert variant="info" className="mb-4">
            Please <Link to="/login">login as a visitor</Link> before confirming a booking.
          </Alert>
        ) : null}

        <Row className="g-4">
          <Col lg={5}>
            <div className="detail-panel h-100">
              <h2 className="h4 fw-bold mb-3">Available cabs</h2>

              {cabTypes.length ? (
                <div className="d-grid gap-3">
                  {cabTypes.map((cab) => (
                    <button
                      type="button"
                      className={`cab-option ${String(cab.id) === String(selectedCabId) ? "is-selected" : ""}`}
                      key={cab.id}
                      onClick={() => setSelectedCabId(String(cab.id))}
                    >
                      <img src={cab.image || fallbackCabImage} alt={cab.name} />
                      <span>
                        <strong>{cab.name}</strong>
                        <small>
                          {cab.capacity} seats {cab.is_ac ? "AC" : "Non-AC"} - {formatMoney(cab.base_fare)} base -{" "}
                          {formatMoney(cab.price_per_km)}/km
                        </small>
                      </span>
                    </button>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  No cab types are available. Add cab types from the admin panel.
                </div>
              )}
            </div>
          </Col>

          <Col lg={7}>
            <div className="detail-panel">
              <Form onSubmit={handleSubmit}>
                <Row className="g-3">
                  <Col md={12}>
                    <Form.Group>
                      <Form.Label>Pickup address</Form.Label>
                      <div className="d-flex gap-2 flex-column flex-sm-row">
                        <Form.Control
                          name="pickup_address"
                          value={formData.pickup_address}
                          onChange={updateField}
                          required
                        />
                        <Button
                          type="button"
                          className="btn-outline-soft flex-shrink-0"
                          onClick={handleUseLiveLocation}
                          disabled={locationLoading}
                        >
                          <FaLocationArrow className="me-2" />
                          {locationLoading ? "Locating" : "Use live"}
                        </Button>
                      </div>
                    </Form.Group>
                  </Col>

                  <Col md={6}>
                    <Form.Group>
                      <Form.Label>Pickup latitude</Form.Label>
                      <Form.Control
                        name="pickup_latitude"
                        value={formData.pickup_latitude}
                        onChange={updateField}
                        placeholder="Auto-filled from live location"
                      />
                    </Form.Group>
                  </Col>

                  <Col md={6}>
                    <Form.Group>
                      <Form.Label>Pickup longitude</Form.Label>
                      <Form.Control
                        name="pickup_longitude"
                        value={formData.pickup_longitude}
                        onChange={updateField}
                        placeholder="Auto-filled from live location"
                      />
                    </Form.Group>
                  </Col>

                  <Col md={12}>
                    <Form.Group>
                      <Form.Label>Tourist place / dropoff</Form.Label>
                      <Form.Control
                        name="dropoff_address"
                        value={formData.dropoff_address}
                        onChange={updateField}
                        placeholder="Select from a place page or type destination"
                        required
                      />
                    </Form.Group>
                  </Col>

                  <Col md={4}>
                    <Form.Group>
                      <Form.Label>Distance km</Form.Label>
                      <Form.Control
                        type="number"
                        min="0"
                        step="0.01"
                        name="distance_km"
                        value={formData.distance_km}
                        onChange={updateField}
                      />
                    </Form.Group>
                  </Col>

                  <Col md={4}>
                    <Form.Group>
                      <Form.Label>Passengers</Form.Label>
                      <Form.Control
                        type="number"
                        min="1"
                        name="num_passengers"
                        value={formData.num_passengers}
                        onChange={updateField}
                        required
                      />
                    </Form.Group>
                  </Col>

                  <Col md={4}>
                    <Form.Group>
                      <Form.Label>Pickup time</Form.Label>
                      <Form.Control
                        type="datetime-local"
                        name="pickup_datetime"
                        value={formData.pickup_datetime}
                        onChange={updateField}
                        required
                      />
                    </Form.Group>
                  </Col>

                  <Col md={12}>
                    <Form.Group>
                      <Form.Label>Special requests</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={3}
                        name="special_requests"
                        value={formData.special_requests}
                        onChange={updateField}
                        placeholder="Optional pickup notes, luggage, accessibility needs"
                      />
                    </Form.Group>
                  </Col>
                </Row>

                <div className="booking-summary mt-4">
                  <div>
                    <FaMapMarkerAlt />
                    <span>{formData.dropoff_address || "Destination not selected"}</span>
                  </div>
                  <div>
                    <FaRupeeSign />
                    <span>{estimatedFare ? `Estimated fare ${formatMoney(estimatedFare)}` : "Fare estimate needs distance"}</span>
                  </div>
                  <div>
                    <FaCalendarCheck />
                    <span>{selectedCab?.name || "Select a cab type"}</span>
                  </div>
                </div>

                <Button
                  type="submit"
                  className="btn-primary-soft mt-4"
                  disabled={submitting || !cabTypes.length}
                >
                  {submitting ? "Creating booking..." : "Confirm cab booking"}
                </Button>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
    </section>
  );
};

export default CabBooking;
