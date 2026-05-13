import {
  Container,
  Card,
} from "react-bootstrap";

import {
  PieChart,
  Pie,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { name: "Morning", value: 400 },
  { name: "Afternoon", value: 300 },
  { name: "Evening", value: 600 },
];

const DayAnalytics = () => {
  return (
    <Container fluid>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          Day-wise Analytics
        </h3>

        <ResponsiveContainer
          width="100%"
          height={400}
        >
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              outerRadius={120}
            />

            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </Card>
    </Container>
  );
};

export default DayAnalytics;