import { Table } from "react-bootstrap";

const CustomTable = ({
  headers,
  data,
}) => {
  return (
    <Table responsive hover>
      <thead>
        <tr>
          {headers.map((header, index) => (
            <th key={index}>{header}</th>
          ))}
        </tr>
      </thead>

      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {Object.values(row).map(
              (value, i) => (
                <td key={i}>{value}</td>
              )
            )}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default CustomTable;