import { useState } from "react";

import {
    Card,
    Form,
    Button,
} from "react-bootstrap";

import {
    FaRobot,
    FaTimes,
} from "react-icons/fa";

const FloatingAIChat = () => {
    const [open, setOpen] =
        useState(false);

    const [message, setMessage] =
        useState("");

    const [chat, setChat] =
        useState([]);

    const sendMessage = () => {
        if (!message.trim()) return;

        setChat([
            ...chat,
            {
                type: "user",
                text: message,
            },
            {
                type: "bot",
                text:
                    "Welcome to Smart Tourism Assistant!",
            },
        ]);

        setMessage("");
    };

    return (
        <>
            {/* Floating Button */}
            <div
                onClick={() => setOpen(!open)}
                style={{
                    position: "fixed",
                    bottom: "30px",
                    right: "30px",
                    width: "65px",
                    height: "65px",
                    borderRadius: "50%",
                    background: "#000",
                    color: "#fff",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    cursor: "pointer",
                    zIndex: 9999,
                    boxShadow:
                        "0 4px 10px rgba(0,0,0,0.3)",
                }}
            >
                {open ? (
                    <FaTimes size={25} />
                ) : (
                    <FaRobot size={25} />
                )}
            </div>

            {/* Chat Box */}
            {open && (
                <Card
                    className="shadow-lg border-0"
                    style={{
                        position: "fixed",
                        bottom: "110px",
                        right: "30px",
                        width: "350px",
                        height: "450px",
                        zIndex: 9999,
                        borderRadius: "20px",
                    }}
                >
                    <Card.Body className="d-flex flex-column">
                        <h5 className="mb-3">
                            AI Travel Assistant
                        </h5>

                        {/* Messages */}
                        <div
                            style={{
                                flex: 1,
                                overflowY: "auto",
                                background: "#f5f5f5",
                                padding: "10px",
                                borderRadius: "10px",
                            }}
                        >
                            {chat.map((msg, index) => (
                                <div
                                    key={index}
                                    className={`d-flex mb-2 ${msg.type === "user"
                                            ? "justify-content-end"
                                            : "justify-content-start"
                                        }`}
                                >
                                    <div
                                        style={{
                                            background:
                                                msg.type === "user"
                                                    ? "#000"
                                                    : "#ddd",

                                            color:
                                                msg.type === "user"
                                                    ? "#fff"
                                                    : "#000",

                                            padding:
                                                "10px 15px",

                                            borderRadius:
                                                "15px",

                                            maxWidth: "75%",
                                        }}
                                    >
                                        {msg.text}
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Input */}
                        <div className="d-flex mt-3">
                            <Form.Control
                                type="text"
                                placeholder="Ask anything..."
                                value={message}
                                onChange={(e) =>
                                    setMessage(
                                        e.target.value
                                    )
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
            )}
        </>
    );
};

export default FloatingAIChat;