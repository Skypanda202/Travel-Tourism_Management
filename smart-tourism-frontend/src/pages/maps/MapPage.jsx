import { GoogleMap, LoadScript, Marker }
from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "500px",
};

const center = {
  lat: 15.2993,
  lng: 74.124,
};

const MapPage = () => {
  return (
    <LoadScript googleMapsApiKey="YOUR_API_KEY">
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={8}
      >
        <Marker position={center} />
      </GoogleMap>
    </LoadScript>
  );
};

export default MapPage;