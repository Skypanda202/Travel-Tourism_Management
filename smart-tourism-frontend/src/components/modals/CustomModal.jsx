import {
  Modal,
  Button,
} from "react-bootstrap";

const CustomModal = ({
  show,
  handleClose,
  title,
  body,
  actionText,
  action,
}) => {
  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>
          {title}
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>{body}</Modal.Body>

      <Modal.Footer>
        <Button
          variant="secondary"
          onClick={handleClose}
        >
          Close
        </Button>

        <Button
          variant="dark"
          onClick={action}
        >
          {actionText}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default CustomModal;