import {
  Row,
  Col,
  Form,
} from "react-bootstrap";

const SearchFilter = ({
  search,
  setSearch,
  category,
  setCategory,
}) => {
  return (
    <Row className="mb-4">
      <Col md={6}>
        <Form.Control
          type="text"
          placeholder="Search places..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />
      </Col>

      <Col md={6}>
        <Form.Select
          value={category}
          onChange={(e) =>
            setCategory(e.target.value)
          }
        >
          <option value="">
            All Categories
          </option>

          <option value="beach">
            Beach
          </option>

          <option value="mountain">
            Mountain
          </option>
        </Form.Select>
      </Col>
    </Row>
  );
};

export default SearchFilter;