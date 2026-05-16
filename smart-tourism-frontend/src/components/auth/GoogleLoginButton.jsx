import { useEffect, useRef, useState } from "react";
import { Button } from "react-bootstrap";
import { toast } from "react-toastify";
import axiosInstance from "../../api/axiosInstance";

const googleScriptId = "google-identity-services";

const GoogleLoginButton = ({ label = "Continue with Google", role = "visitor", onSuccess }) => {
  const buttonRef = useRef(null);
  const [ready, setReady] = useState(false);
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  useEffect(() => {
    if (!clientId) {
      return;
    }

    const existingScript = document.getElementById(googleScriptId);
    if (existingScript) {
      queueMicrotask(() => setReady(true));
      return;
    }

    const script = document.createElement("script");
    script.id = googleScriptId;
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = () => setReady(true);
    document.body.appendChild(script);
  }, [clientId]);

  useEffect(() => {
    if (!ready || !clientId || !window.google || !buttonRef.current) {
      return;
    }

    window.google.accounts.id.initialize({
      client_id: clientId,
      callback: async ({ credential }) => {
        try {
          const response = await axiosInstance.post("google/", {
            credential,
            role,
          });
          onSuccess(response.data);
        } catch (error) {
          console.log(error);
          toast.error(error.response?.data?.message || "Google login failed");
        }
      },
    });

    window.google.accounts.id.renderButton(buttonRef.current, {
      theme: "outline",
      size: "large",
      width: buttonRef.current.offsetWidth || 320,
      text: "continue_with",
    });
  }, [clientId, onSuccess, ready, role]);

  if (!clientId) {
    return (
      <Button className="btn-outline-soft w-100" disabled>
        Google login not configured
      </Button>
    );
  }

  return (
    <div aria-label={label} className="w-100">
      <div ref={buttonRef} />
    </div>
  );
};

export default GoogleLoginButton;
