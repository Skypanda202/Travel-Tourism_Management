import {
  Container,
  Card,
} from "react-bootstrap";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { year: "2022", visitors: 5000 },
  { year: "2023", visitors: 8000 },
  { year: "2024", visitors: 12000 },
];

const YearAnalytics = () => {
  return (
    <Container fluid>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          Year-wise Analytics
        </h3>

        <ResponsiveContainer
          width="100%"
          height={400}
        >
          <LineChart data={data}>
            <XAxis dataKey="year" />

            <YAxis />

            <Tooltip />

            <Line dataKey="visitors" />
          </LineChart>
        </ResponsiveContainer>
      </Card>
    </Container>
  );
};

export default YearAnalytics;