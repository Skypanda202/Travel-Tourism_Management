import { Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import { FaHeart, FaMapMarkerAlt, FaRupeeSign, FaStar } from "react-icons/fa";
import { useState } from "react";
import axiosInstance from "../../api/axiosInstance";

const fallbackImage =
  "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80";

const PlaceCard = ({ place }) => {
  const [isFavorited, setIsFavorited] = useState(Boolean(place.is_favorited));
  const image = place.cover_image_url || place.image || fallbackImage;
  const location = [place.city, place.state || place.country].filter(Boolean).join(", ");
  const description =
    place.short_desc || place.description || "A destination ready to be explored.";
  const detailsPath = `/place/${place.slug || place.id}`;

  const handleFavorite = async () => {
    if (!localStorage.getItem("token")) {
      toast.info("Please login as a visitor to save favorites.");
      return;
    }

    try {
      const response = await axiosInstance.post(`places/${place.slug || place.id}/favorite/`);
      const nextValue = response.data.data?.is_favorited ?? !isFavorited;
      setIsFavorited(nextValue);
      toast.success(nextValue ? "Added to favorites" : "Removed from favorites");
    } catch (error) {
      console.log(error);
      toast.error("Could not update favorite.");
    }
  };

  return (
    <article className="place-card">
      <img className="place-card-media" src={image} alt={place.name} />

      <div className="place-card-body">
        <div className="d-flex justify-content-between gap-3 mb-2">
          <h3 className="place-card-title">{place.name}</h3>
          {place.avg_rating ? (
            <span className="badge badge-soft px-2 py-1">
              <FaStar className="me-1" />
              {Number(place.avg_rating).toFixed(1)}
            </span>
          ) : null}
        </div>

        <p className="place-meta mb-3">
          <FaMapMarkerAlt className="me-2" />
          {location || "Location available on details"}
        </p>

        <p className="mb-4 text-secondary">
          {description.length > 120 ? `${description.slice(0, 120)}...` : description}
        </p>

        <div className="d-flex align-items-center justify-content-between gap-3">
          <span className="fw-bold text-success">
            {place.is_free ? (
              "Free entry"
            ) : (
              <>
                <FaRupeeSign className="me-1" />
                {place.entry_fee || "Check fee"}
              </>
            )}
          </span>

          <div className="d-flex gap-2">
            <Button
              type="button"
              className="btn-outline-soft"
              aria-label={isFavorited ? "Remove favorite" : "Add favorite"}
              onClick={handleFavorite}
            >
              <FaHeart className={isFavorited ? "text-danger" : ""} />
            </Button>

            <Button as={Link} to={detailsPath} className="btn-primary-soft">
              View
            </Button>
          </div>
        </div>
      </div>
    </article>
  );
};

export default PlaceCard;
