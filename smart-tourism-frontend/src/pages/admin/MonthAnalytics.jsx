import {
  Container,
  Card,
} from "react-bootstrap";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { month: "Jan", users: 500 },
  { month: "Feb", users: 900 },
  { month: "Mar", users: 1500 },
];

const MonthAnalytics = () => {
  return (
    <Container fluid>
      <Card className="shadow border-0 rounded-4 p-4">
        <h3 className="mb-4">
          Month-wise Analytics
        </h3>

        <ResponsiveContainer
          width="100%"
          height={400}
        >
          <BarChart data={data}>
            <XAxis dataKey="month" />

            <YAxis />

            <Tooltip />

            <Bar dataKey="users" />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </Container>
  );
};

export default MonthAnalytics;