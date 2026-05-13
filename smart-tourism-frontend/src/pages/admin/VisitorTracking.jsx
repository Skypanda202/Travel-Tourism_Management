import {
  Container,
  Card,
} from "react-bootstrap";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const visitorData = [
  { day: "Mon", visitors: 500 },
  { day: "Tue", visitors: 800 },
  { day: "Wed", visitors: 950 },
  { day: "Thu", visitors: 1200 },
  { day: "Fri", visitors: 1800 },
];

const VisitorTracking = () => {
  return (
    <Container fluid>
      <h2 className="fw-bold mb-4">
        Visitor Tracking
      </h2>

      <Card className="shadow border-0 rounded-4 p-4">
        <ResponsiveContainer
          width="100%"
          height={400}
        >
          <AreaChart data={visitorData}>
            <XAxis dataKey="day" />

            <YAxis />

            <Tooltip />

            <Area
              type="monotone"
              dataKey="visitors"
            />
          </AreaChart>
        </ResponsiveContainer>
      </Card>
    </Container>
  );
};

export default VisitorTracking;