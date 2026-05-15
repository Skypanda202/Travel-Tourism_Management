import { useEffect, useRef, useState } from "react";
import { Button, Container, Form, Spinner } from "react-bootstrap";
import { FaPaperPlane } from "react-icons/fa";
import { sendAIMessage } from "../../services/aiService";

const AIChatAssistant = () => {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([
    {
      type: "bot",
      text: "Tell me where you are starting from, what kind of places you like, and how much time you have.",
    },
  ]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat, loading]);

  const sendMessage = async () => {
    const nextMessage = message.trim();
    if (!nextMessage || loading) {
      return;
    }

    setChat((current) => [...current, { type: "user", text: nextMessage }]);
    setMessage("");
    setLoading(true);

    try {
      const response = await sendAIMessage(nextMessage);
      setChat((current) => [
        ...current,
        {
          type: "bot",
          text: response.reply || "I could not prepare a reply right now. Please try again.",
        },
      ]);
    } catch (error) {
      console.log(error);
      setChat((current) => [
        ...current,
        {
          type: "bot",
          text: "The assistant is temporarily unavailable. Please try again in a moment.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage();
  };

  return (
    <section className="section-band ai-page">
      <Container>
        <div className="ai-shell">
          <div className="ai-header">
            <span className="section-eyebrow">AI travel assistant</span>
            <h1>Plan a better Kalahandi visit</h1>
          </div>

          <div className="ai-chat-window" aria-live="polite">
            {chat.map((item, index) => (
              <div className={`ai-message-row ${item.type === "user" ? "is-user" : ""}`} key={`${item.type}-${index}`}>
                <div className={`ai-message ${item.type === "user" ? "is-user" : "is-bot"}`}>
                  {item.text}
                </div>
              </div>
            ))}

            {loading ? (
              <div className="ai-message-row">
                <div className="ai-message is-bot">
                  <Spinner animation="border" size="sm" className="me-2" />
                  Preparing answer...
                </div>
              </div>
            ) : null}
            <div ref={chatEndRef} />
          </div>

          <Form className="ai-input-bar" onSubmit={handleSubmit}>
            <Form.Control
              type="text"
              placeholder="Ask about places, routes, timing, food, or trip ideas"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
            />
            <Button type="submit" className="btn-primary-soft" disabled={loading || !message.trim()}>
              <FaPaperPlane className="me-sm-2" />
              <span className="d-none d-sm-inline">Send</span>
            </Button>
          </Form>
        </div>
      </Container>
    </section>
  );
};

export default AIChatAssistant;
