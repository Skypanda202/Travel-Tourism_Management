import {
  Container,
  Card,
  Form,
  Button,
  Spinner,
} from "react-bootstrap";

import { useState } from "react";

import { sendAIMessage }
from "../../services/aiService";

const AIChatAssistant = () => {
  const [message, setMessage] =
    useState("");

  const [chat, setChat] = useState([]);

  const [loading, setLoading] =
    useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = {
      type: "user",
      text: message,
    };

    setChat((prev) => [
      ...prev,
      userMessage,
    ]);

    setLoading(true);

    try {
      const response =
        await sendAIMessage(message);

      const botMessage = {
        type: "bot",
        text: response.reply,
      };

      setChat((prev) => [
        ...prev,
        botMessage,
      ]);
    } catch (error) {
      console.log(error);
    }

    setLoading(false);

    setMessage("");
  };

  return (
    <Container className="py-5">
      <Card className="shadow-lg border-0 rounded-4">
        <Card.Body>
          <h3 className="mb-4">
            AI Travel Assistant
          </h3>

          {/* Chat Window */}
          <div
            style={{
              height: "450px",
              overflowY: "auto",
              background: "#f5f5f5",
              padding: "20px",
              borderRadius: "15px",
            }}
          >
            {chat.map((msg, index) => (
              <div
                key={index}
                className={`d-flex mb-3 ${
                  msg.type === "user"
                    ? "justify-content-end"
                    : "justify-content-start"
                }`}
              >
                <div
                  style={{
                    background:
                      msg.type === "user"
                        ? "#000"
                        : "#e4e4e4",

                    color:
                      msg.type === "user"
                        ? "#fff"
                        : "#000",

                    padding: "12px 18px",

                    borderRadius: "20px",

                    maxWidth: "70%",
                  }}
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {loading && (
              <div className="text-center">
                <Spinner animation="border" />
              </div>
            )}
          </div>

          {/* Input */}
          <div className="d-flex mt-4">
            <Form.Control
              type="text"
              placeholder="Ask your travel question..."
              value={message}
              onChange={(e) =>
                setMessage(e.target.value)
              }
            />

            <Button
              variant="dark"
              className="ms-2"
              onClick={sendMessage}
            >
              Send
            </Button>
          </div>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default AIChatAssistant;