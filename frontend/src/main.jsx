import * as React from "react";
import * as ReactDOM from "react-dom/client";
import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider } from "@mui/material/styles";
import App from "./app/App";
import { getTheme } from "./theme";

function AppWithTheme() {
  const [mode, setMode] = React.useState(() => {
    return localStorage.getItem("themeMode") || "light";
  });

  const theme = React.useMemo(() => getTheme(mode), [mode]);

  const toggleColorMode = React.useCallback(() => {
    setMode((prevMode) => {
      const newMode = prevMode === "light" ? "dark" : "light";
      localStorage.setItem("themeMode", newMode);
      return newMode;
    });
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div
        style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
      >
        <App toggleColorMode={toggleColorMode} mode={mode} />
      </div>
    </ThemeProvider>
  );
}

const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <AppWithTheme />
  </React.StrictMode>
);
