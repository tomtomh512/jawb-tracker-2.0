import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "../../packages/shared-ui/src/App.jsx";
import { SettingsProvider } from "../../packages/shared-ui/src/context/SettingsContext.jsx";
import { ToastProvider } from "../../packages/shared-ui/src/context/ToastContext.jsx";
import "../../packages/shared-ui/src/styles/index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <SettingsProvider>
      <ToastProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ToastProvider>
    </SettingsProvider>
  </React.StrictMode>
);
