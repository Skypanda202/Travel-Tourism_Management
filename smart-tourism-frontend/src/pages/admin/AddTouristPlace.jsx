import { useEffect, useState } from "react";
import { Alert, Button, Col, Form, Row, Spinner } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import axiosInstance from "../../api/axiosInstance";

const defaultMapCenter = { lat: 20.2376, lon: 84.27 };

const formatCoordinate = (value) => Number(value).toFixed(6);

const indianStates = [
  "Andhra Pradesh",
  "Arunachal Pradesh",
  "Assam",
  "Bihar",
  "Chhattisgarh",
  "Goa",
  "Gujarat",
  "Haryana",
  "Himachal Pradesh",
  "Jharkhand",
  "Karnataka",
  "Kerala",
  "Madhya Pradesh",
  "Maharashtra",
  "Manipur",
  "Meghalaya",
  "Mizoram",
  "Nagaland",
  "Odisha",
  "Punjab",
  "Rajasthan",
  "Sikkim",
  "Tamil Nadu",
  "Telangana",
  "Tripura",
  "Uttar Pradesh",
  "Uttarakhand",
  "West Bengal",
  "Andaman and Nicobar Islands",
  "Chandigarh",
  "Dadra and Nagar Haveli and Daman and Diu",
  "Delhi",
  "Jammu and Kashmir",
  "Ladakh",
  "Lakshadweep",
  "Puducherry",
];

const initialFormData = {
  name: "",
  short_desc: "",
  description: "",
  category_id: "",
  address: "",
  city: "",
  state: "Odisha",
  country: "India",
  latitude: "",
  longitude: "",
  entry_fee: "0",
  opening_time: "",
  closing_time: "",
  open_days: "",
  best_time_to_visit: "",
  cover_image: null,
};

const AddTouristPlace = () => {
  const navigate = useNavigate();
  const { slug } = useParams();
  const isEditMode = Boolean(slug);
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState([]);
  const [locationSearch, setLocationSearch] = useState("");
  const [locationLoading, setLocationLoading] = useState(false);
  const [locationError, setLocationError] = useState("");
  const [locationResults, setLocationResults] = useState([]);
  const [mapCenter, setMapCenter] = useState(defaultMapCenter);
  const [markerPosition, setMarkerPosition] = useState(null);
  const [preview, setPreview] = useState(null);
  const [galleryPreviews, setGalleryPreviews] = useState([]);
  const [galleryImages, setGalleryImages] = useState([]);
  const [formData, setFormData] = useState(initialFormData);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axiosInstance.get("places/categories/");
        setCategories(response.data.results || response.data.data || response.data || []);
      } catch (error) {
        console.log(error);
      }
    };

    fetchCategories();
  }, []);

  useEffect(() => {
    if (!slug) {
      return;
    }

    const fetchPlace = async () => {
      try {
        setLoading(true);
        const response = await axiosInstance.get(`places/${slug}/`);
        const place = response.data.data || response.data;
        const nextPosition = {
          lat: Number(place.latitude),
          lon: Number(place.longitude),
        };

        setFormData({
          name: place.name || "",
          short_desc: place.short_desc || "",
          description: place.description || "",
          category_id: place.category?.id || place.category || "",
          address: place.address || "",
          city: place.city || "",
          state: place.state || "Odisha",
          country: place.country || "India",
          latitude: place.latitude || "",
          longitude: place.longitude || "",
          entry_fee: place.entry_fee || "0",
          opening_time: place.opening_time || "",
          closing_time: place.closing_time || "",
          open_days: place.open_days || "",
          best_time_to_visit: place.best_time_to_visit || "",
          cover_image: null,
        });
        setMapCenter(nextPosition);
        setMarkerPosition(nextPosition);
        setPreview(place.cover_image_url || null);
        setLocationSearch(place.address || place.name || "");
      } catch (error) {
        console.log(error);
        toast.error("Could not load place details");
      } finally {
        setLoading(false);
      }
    };

    fetchPlace();
  }, [slug]);

  const getMapUrl = () => {
    const lat = Number(markerPosition?.lat || mapCenter.lat);
    const lon = Number(markerPosition?.lon || mapCenter.lon);
    const latDelta = 0.02;
    const lonDelta = 0.03;
    const bbox = [
      lon - lonDelta,
      lat - latDelta,
      lon + lonDelta,
      lat + latDelta,
    ].join(",");

    return `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik&marker=${lat},${lon}`;
  };

  const handleLocationSearch = async () => {
    if (!locationSearch.trim()) {
      toast.warning("Enter a place, landmark, or address to search.");
      return;
    }

    try {
      setLocationLoading(true);
      setLocationError("");
      const params = new URLSearchParams({
        q: `${locationSearch}, India`,
        format: "json",
        addressdetails: "1",
        limit: "6",
      });
      const response = await fetch(`https://nominatim.openstreetmap.org/search?${params}`);

      if (!response.ok) {
        throw new Error("Location search failed");
      }

      const results = await response.json();
      setLocationResults(results);

      if (!results.length) {
        setLocationError("No matching location found. Try a nearby landmark or a fuller address.");
      }
    } catch (error) {
      console.log(error);
      setLocationError("Location search is temporarily unavailable. Try again in a moment.");
    } finally {
      setLocationLoading(false);
    }
  };

  const applyLocationResult = (result) => {
    const address = result.address || {};
    const nextPosition = {
      lat: Number(formatCoordinate(result.lat)),
      lon: Number(formatCoordinate(result.lon)),
    };

    setMarkerPosition(nextPosition);
    setMapCenter(nextPosition);
    setLocationResults([]);
    setLocationSearch(result.display_name);
    setFormData((current) => ({
      ...current,
      address: result.display_name || current.address,
      city:
        address.city ||
        address.town ||
        address.village ||
        address.county ||
        current.city,
      state: address.state || current.state,
      country: address.country || current.country,
      latitude: formatCoordinate(nextPosition.lat),
      longitude: formatCoordinate(nextPosition.lon),
    }));
  };

  const handleChange = (event) => {
    const { name, value, files } = event.target;

    if (name === "cover_image") {
      const file = files?.[0] || null;
      setFormData((current) => ({
        ...current,
        cover_image: file,
      }));
      setPreview(file ? URL.createObjectURL(file) : null);
      return;
    }

    if (name === "gallery_images") {
      const selectedFiles = Array.from(files || []);
      setGalleryImages(selectedFiles);
      setGalleryPreviews(selectedFiles.map((file) => URL.createObjectURL(file)));
      return;
    }

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!formData.latitude || !formData.longitude) {
      toast.error("Search or pin the location on the map before saving.");
      return;
    }

    setLoading(true);

    const data = new FormData();

    Object.entries(formData).forEach(([key, value]) => {
      if (value !== "" && value !== null) {
        data.append(key, value);
      }
    });

    try {
      const response = await axiosInstance[isEditMode ? "patch" : "post"](
        isEditMode ? `places/${slug}/` : "places/",
        data,
        {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        },
      );

      const createdPlace = response.data.data || response.data;
      const placeSlug = createdPlace.slug;

      if (placeSlug && galleryImages.length) {
        const galleryData = new FormData();
        galleryImages.forEach((image) => galleryData.append("images", image));

        await axiosInstance.post(`places/${placeSlug}/upload_images/`, galleryData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
      }

      toast.success(isEditMode ? "Tourist place updated successfully" : "Tourist place added successfully");
      setFormData(initialFormData);
      setPreview(null);
      setGalleryImages([]);
      setGalleryPreviews([]);
      setMarkerPosition(null);
      setMapCenter(defaultMapCenter);
      setLocationSearch("");
      setLocationResults([]);
      if (isEditMode) {
        navigate("/admin/places");
      }
    } catch (error) {
      console.log(error);
      const message =
        error.response?.data?.error?.message ||
        error.response?.data?.message ||
        isEditMode ? "Failed to update tourist place" : "Failed to add tourist place";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="detail-panel">
      <span className="section-eyebrow">Admin details</span>
      <h1 className="h2 fw-bold mt-2 mb-2">
        {isEditMode ? "Edit tourist place" : "Add tourist place"}
      </h1>
      <p className="section-copy mb-4">
        Fill the destination details below. Required fields match the backend
        place model so the record can be published immediately.
      </p>

      <Form onSubmit={handleSubmit}>
        <Row className="g-3">
          <Col md={6}>
            <Form.Group>
              <Form.Label>Place name</Form.Label>
              <Form.Control
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Enter place name"
                required
              />
            </Form.Group>
          </Col>

          <Col md={6}>
            <Form.Group>
              <Form.Label>Category</Form.Label>
              <Form.Select
                name="category_id"
                value={formData.category_id}
                onChange={handleChange}
                required
              >
                <option value="">Select category</option>
                {categories.map((category) => (
                  <option value={category.id} key={category.id}>
                    {category.name}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>

          <Col md={12}>
            <Form.Group>
              <Form.Label>Short description</Form.Label>
              <Form.Control
                type="text"
                name="short_desc"
                value={formData.short_desc}
                onChange={handleChange}
                placeholder="A short summary for cards"
              />
            </Form.Group>
          </Col>

          <Col md={12}>
            <Form.Group>
              <Form.Label>Description</Form.Label>
              <Form.Control
                as="textarea"
                rows={4}
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe the destination"
                required
              />
            </Form.Group>
          </Col>

          <Col md={12}>
            <Form.Group>
              <Form.Label>Search location</Form.Label>
              <div className="d-flex gap-2">
                <Form.Control
                  type="search"
                  value={locationSearch}
                  onChange={(event) => setLocationSearch(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      event.preventDefault();
                      handleLocationSearch();
                    }
                  }}
                  placeholder="Search temple, waterfall, fort, village, or landmark"
                  aria-label="Search location with OpenStreetMap"
                />
                <Button
                  type="button"
                  className="btn-outline-soft"
                  onClick={handleLocationSearch}
                  disabled={locationLoading}
                >
                  {locationLoading ? "Searching..." : "Search"}
                </Button>
              </div>
              <Form.Text>
                Free OpenStreetMap search. Choose a result to place the pin.
              </Form.Text>
            </Form.Group>
          </Col>

          {locationError ? (
            <Col md={12}>
              <Alert variant="warning" className="mb-0">
                {locationError}
              </Alert>
            </Col>
          ) : null}

          {locationResults.length ? (
            <Col md={12}>
              <div className="search-panel">
                <h2 className="h6 fw-bold mb-3">Choose location</h2>
                <div className="d-grid gap-2">
                  {locationResults.map((result) => (
                    <Button
                      type="button"
                      className="btn-outline-soft text-start"
                      key={result.place_id}
                      onClick={() => applyLocationResult(result)}
                    >
                      {result.display_name}
                    </Button>
                  ))}
                </div>
              </div>
            </Col>
          ) : null}

          <Col md={12}>
            <Form.Group>
              <Form.Label>Selected address</Form.Label>
              <Form.Control
                as="textarea"
                rows={2}
                name="address"
                value={formData.address}
                onChange={handleChange}
                placeholder="Full address"
                required
              />
            </Form.Group>
          </Col>

          <Col md={4}>
            <Form.Group>
              <Form.Label>City</Form.Label>
              <Form.Control
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>

          <Col md={4}>
            <Form.Group>
              <Form.Label>State</Form.Label>
              <Form.Select
                name="state"
                value={formData.state}
                onChange={handleChange}
                required
              >
                <option value="">Select state</option>
                {indianStates.map((stateName) => (
                  <option value={stateName} key={stateName}>
                    {stateName}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>

          <Col md={4}>
            <Form.Group>
              <Form.Label>Country</Form.Label>
              <Form.Control
                type="text"
                name="country"
                value={formData.country}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>

          <Col md={12}>
            <Form.Group>
              <Form.Label>Pin exact location</Form.Label>
              <iframe
                title="Selected tourist place location"
                src={getMapUrl()}
                width="100%"
                height="360"
                className="border rounded"
                loading="lazy"
              />
              <Form.Text>
                The selected OpenStreetMap result is saved as the place location.
                Search a more specific landmark if the pin needs adjustment.
              </Form.Text>
            </Form.Group>
          </Col>

          <Col md={4}>
            <Form.Group>
              <Form.Label>Entry fee</Form.Label>
              <Form.Control
                type="number"
                min="0"
                step="0.01"
                name="entry_fee"
                value={formData.entry_fee}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>

          <Col md={4}>
            <Form.Group>
              <Form.Label>Opening time</Form.Label>
              <Form.Control
                type="time"
                name="opening_time"
                value={formData.opening_time}
                onChange={handleChange}
              />
            </Form.Group>
          </Col>

          <Col md={4}>
            <Form.Group>
              <Form.Label>Closing time</Form.Label>
              <Form.Control
                type="time"
                name="closing_time"
                value={formData.closing_time}
                onChange={handleChange}
              />
            </Form.Group>
          </Col>

          <Col md={4}>
            <Form.Group>
              <Form.Label>Open days</Form.Label>
              <Form.Control
                type="text"
                name="open_days"
                value={formData.open_days}
                onChange={handleChange}
                placeholder="Mon-Sun"
              />
            </Form.Group>
          </Col>

          <Col md={6}>
            <Form.Group>
              <Form.Label>Best time to visit</Form.Label>
              <Form.Control
                type="text"
                name="best_time_to_visit"
                value={formData.best_time_to_visit}
                onChange={handleChange}
                placeholder="October to February"
              />
            </Form.Group>
          </Col>

          <Col md={6}>
            <Form.Group>
              <Form.Label>Cover image</Form.Label>
              <Form.Control
                type="file"
                name="cover_image"
                accept="image/*"
                onChange={handleChange}
              />
            </Form.Group>
          </Col>

          <Col md={12}>
            <Form.Group>
              <Form.Label>Gallery images</Form.Label>
              <Form.Control
                type="file"
                name="gallery_images"
                accept="image/*"
                multiple
                onChange={handleChange}
              />
              <Form.Text>
                Add extra photos for the destination detail gallery.
              </Form.Text>
            </Form.Group>
          </Col>
        </Row>

        {preview ? (
          <div className="mt-4">
            <img
              src={preview}
              alt="Selected place preview"
              className="detail-image"
              style={{ minHeight: "220px", maxHeight: "320px" }}
            />
          </div>
        ) : null}

        {galleryPreviews.length ? (
          <Row className="g-3 mt-3">
            {galleryPreviews.map((imageUrl) => (
              <Col md={4} key={imageUrl}>
                <img
                  src={imageUrl}
                  alt="Selected gallery preview"
                  className="place-card-media rounded"
                />
              </Col>
            ))}
          </Row>
        ) : null}

        <Button
          type="submit"
          className="btn-primary-soft mt-4 px-4"
          disabled={loading}
        >
          {loading ? (
            <>
              <Spinner animation="border" size="sm" className="me-2" />
              Saving...
            </>
          ) : (
            isEditMode ? "Update place details" : "Add place details"
          )}
        </Button>
      </Form>
    </div>
  );
};

export default AddTouristPlace;
