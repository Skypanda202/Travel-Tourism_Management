import {
  Container,
  Row,
  Col,
  Card,
} from "react-bootstrap";

const WeatherPage = () => {
  const weatherData = [
    {
      city: "Goa",
      temp: "32°C",
      condition: "Sunny",
    },
    {
      city: "Manali",
      temp: "15°C",
      condition: "Cloudy",
    },
  ];

  return (
    <Container className="py-5">
      <h2 className="mb-5 text-center">
        Weather Forecast
      </h2>

      <Row>
        {weatherData.map((weather, index) => (
          <Col md={4} key={index}>
            <Card className="shadow border-0 rounded-4 mb-4 p-4 text-center">
              <h3>{weather.city}</h3>

              <h1>{weather.temp}</h1>

              <p>{weather.condition}</p>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default WeatherPage;