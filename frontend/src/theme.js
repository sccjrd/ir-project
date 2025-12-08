import { createTheme } from "@mui/material/styles";
import { red } from "@mui/material/colors";

export const getTheme = (mode) =>
  createTheme({
    cssVariables: true,
    palette: {
      mode: mode,
      primary: {
        main: "#556cd6",
      },
      secondary: {
        main: "#19857b",
      },
      error: {
        main: red.A400,
      },
    },
    typography: {
      fontFamily: [
        '"Noto Sans"',
        "-apple-system",
        "BlinkMacSystemFont",
        '"Segoe UI"',
        "Roboto",
        '"Helvetica Neue"',
        "Arial",
        "sans-serif",
        '"Apple Color Emoji"',
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
      ].join(","),
    },
  });

const theme = getTheme("light");
export default theme;
