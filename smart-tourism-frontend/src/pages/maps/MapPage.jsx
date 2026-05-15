import { Container } from "react-bootstrap";

const kalahandiMapUrl =
  "https://www.openstreetmap.org/export/embed.html?bbox=82.2,19.0,84.4,20.8&layer=mapnik&marker=19.9074,83.1647";

const MapPage = () => {
  return (
    <section className="section-band">
      <Container>
        <span className="section-eyebrow">Explore map</span>
        <h1 className="section-title">Kalahandi map</h1>
        <p className="section-copy mb-4">
          OpenStreetMap is used here, so the public map works without a Google
          API key.
        </p>

        <div className="detail-panel">
          <iframe
            title="Kalahandi tourism map"
            src={kalahandiMapUrl}
            width="100%"
            height="560"
            className="border rounded"
            loading="lazy"
          />
        </div>
      </Container>
    </section>
  );
};

export default MapPage;
