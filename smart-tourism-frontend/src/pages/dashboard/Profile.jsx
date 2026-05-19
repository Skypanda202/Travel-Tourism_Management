import { useEffect, useState } from "react";
import { Alert, Button, Col, Container, Form, Row, Spinner } from "react-bootstrap";
import { toast } from "react-toastify";
import axiosInstance from "../../api/axiosInstance";

const initialAccountForm = {
  first_name: "",
  last_name: "",
  phone_number: "",
  city: "",
  country: "",
  date_of_birth: "",
  bio: "",
  preferred_language: "en",
  newsletter_opt_in: false,
};

const initialTravelForm = {
  travel_style: "",
  instagram_handle: "",
  twitter_handle: "",
};

const travelStyles = [
  { value: "", label: "Choose travel style" },
  { value: "adventure", label: "Adventure" },
  { value: "leisure", label: "Leisure" },
  { value: "cultural", label: "Cultural" },
  { value: "business", label: "Business" },
  { value: "family", label: "Family" },
];

const Profile = () => {
  const [accountForm, setAccountForm] = useState(initialAccountForm);
  const [travelForm, setTravelForm] = useState(initialTravelForm);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [savingAccount, setSavingAccount] = useState(false);
  const [savingTravel, setSavingTravel] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadProfile = async () => {
      try {
        setLoading(true);
        setError("");
        const [profileResponse, travelResponse] = await Promise.all([
          axiosInstance.get("users/profile/"),
          axiosInstance.get("users/visitor-profile/"),
        ]);

        const account = profileResponse.data.data || {};
        const travel = travelResponse.data.data || {};

        setProfile(account);
        setAccountForm({
          first_name: account.first_name || "",
          last_name: account.last_name || "",
          phone_number: account.phone_number || "",
          city: account.city || "",
          country: account.country || "",
          date_of_birth: account.date_of_birth || "",
          bio: account.bio || "",
          preferred_language: account.preferred_language || "en",
          newsletter_opt_in: Boolean(account.newsletter_opt_in),
        });
        setTravelForm({
          travel_style: travel.travel_style || "",
          instagram_handle: travel.instagram_handle || "",
          twitter_handle: travel.twitter_handle || "",
        });
      } catch (profileError) {
        console.log(profileError);
        setError("Could not load profile details. Please login again.");
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, []);

  const updateAccountField = (event) => {
    const { checked, name, type, value } = event.target;
    setAccountForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const updateTravelField = (event) => {
    const { name, value } = event.target;
    setTravelForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const saveAccount = async (event) => {
    event.preventDefault();

    try {
      setSavingAccount(true);
      const response = await axiosInstance.patch("users/profile/", accountForm);
      setProfile(response.data.data || null);
      toast.success("Profile updated");
    } catch (saveError) {
      console.log(saveError);
      toast.error(saveError.response?.data?.message || "Could not update profile");
    } finally {
      setSavingAccount(false);
    }
  };

  const saveTravel = async (event) => {
    event.preventDefault();

    try {
      setSavingTravel(true);
      await axiosInstance.patch("users/visitor-profile/", travelForm);
      toast.success("Travel preferences updated");
    } catch (saveError) {
      console.log(saveError);
      toast.error(saveError.response?.data?.message || "Could not update preferences");
    } finally {
      setSavingTravel(false);
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
        <Row className="align-items-end mb-4 g-3">
          <Col lg={8}>
            <span className="section-eyebrow">Profile</span>
            <h1 className="section-title">Personal details</h1>
            <p className="section-copy">
              Keep your contact details and travel preferences ready for bookings,
              reviews, and trip planning.
            </p>
          </Col>
          <Col lg={4} className="text-lg-end">
            <div className="detail-panel profile-summary">
              <strong>{profile?.full_name || profile?.email}</strong>
              <span>{profile?.email}</span>
            </div>
          </Col>
        </Row>

        {error ? <Alert variant="warning">{error}</Alert> : null}

        <Row className="g-4">
          <Col lg={7}>
            <div className="detail-panel">
              <h2 className="h4 fw-bold mb-3">Account information</h2>
              <Form onSubmit={saveAccount}>
                <Row className="g-3">
                  <Col md={6}>
                    <Form.Label>First name</Form.Label>
                    <Form.Control
                      name="first_name"
                      value={accountForm.first_name}
                      onChange={updateAccountField}
                    />
                  </Col>
                  <Col md={6}>
                    <Form.Label>Last name</Form.Label>
                    <Form.Control
                      name="last_name"
                      value={accountForm.last_name}
                      onChange={updateAccountField}
                    />
                  </Col>
                  <Col md={6}>
                    <Form.Label>Phone</Form.Label>
                    <Form.Control
                      name="phone_number"
                      value={accountForm.phone_number}
                      onChange={updateAccountField}
                      placeholder="+919999999999"
                    />
                  </Col>
                  <Col md={6}>
                    <Form.Label>Date of birth</Form.Label>
                    <Form.Control
                      type="date"
                      name="date_of_birth"
                      value={accountForm.date_of_birth}
                      onChange={updateAccountField}
                    />
                  </Col>
                  <Col md={6}>
                    <Form.Label>City</Form.Label>
                    <Form.Control
                      name="city"
                      value={accountForm.city}
                      onChange={updateAccountField}
                    />
                  </Col>
                  <Col md={6}>
                    <Form.Label>Country</Form.Label>
                    <Form.Control
                      name="country"
                      value={accountForm.country}
                      onChange={updateAccountField}
                    />
                  </Col>
                  <Col md={6}>
                    <Form.Label>Language</Form.Label>
                    <Form.Select
                      name="preferred_language"
                      value={accountForm.preferred_language}
                      onChange={updateAccountField}
                    >
                      <option value="en">English</option>
                      <option value="hi">Hindi</option>
                      <option value="or">Odia</option>
                    </Form.Select>
                  </Col>
                  <Col md={6} className="d-flex align-items-end">
                    <Form.Check
                      type="switch"
                      id="newsletter-opt-in"
                      name="newsletter_opt_in"
                      checked={accountForm.newsletter_opt_in}
                      onChange={updateAccountField}
                      label="Send travel updates"
                    />
                  </Col>
                  <Col xs={12}>
                    <Form.Label>Bio</Form.Label>
                    <Form.Control
                      as="textarea"
                      rows={4}
                      name="bio"
                      value={accountForm.bio}
                      onChange={updateAccountField}
                    />
                  </Col>
                </Row>

                <Button className="btn-primary-soft mt-4" type="submit" disabled={savingAccount}>
                  {savingAccount ? "Saving..." : "Save profile"}
                </Button>
              </Form>
            </div>
          </Col>

          <Col lg={5}>
            <div className="detail-panel">
              <h2 className="h4 fw-bold mb-3">Travel preferences</h2>
              <Form onSubmit={saveTravel}>
                <Form.Group className="mb-3">
                  <Form.Label>Travel style</Form.Label>
                  <Form.Select
                    name="travel_style"
                    value={travelForm.travel_style}
                    onChange={updateTravelField}
                  >
                    {travelStyles.map((style) => (
                      <option key={style.value} value={style.value}>
                        {style.label}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Instagram</Form.Label>
                  <Form.Control
                    name="instagram_handle"
                    value={travelForm.instagram_handle}
                    onChange={updateTravelField}
                    placeholder="@traveller"
                  />
                </Form.Group>

                <Form.Group className="mb-4">
                  <Form.Label>Twitter / X</Form.Label>
                  <Form.Control
                    name="twitter_handle"
                    value={travelForm.twitter_handle}
                    onChange={updateTravelField}
                    placeholder="@traveller"
                  />
                </Form.Group>

                <Button className="btn-outline-soft" type="submit" disabled={savingTravel}>
                  {savingTravel ? "Saving..." : "Save preferences"}
                </Button>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
    </section>
  );
};

export default Profile;
