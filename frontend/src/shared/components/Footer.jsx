import { Box, Typography, Link, IconButton } from "@mui/material";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";

function Footer({ toggleColorMode, mode }) {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        mt: 6,
        textAlign: "center",
        borderTop: 1,
        borderColor: "divider",
        position: "relative",
      }}
    >
      {/* Dark mode toggle in top right of footer */}
      <Box
        sx={{
          position: "absolute",
          right: 16,
          top: "50%",
          transform: "translateY(-50%)",
        }}
      >
        <IconButton
          onClick={toggleColorMode}
          color="inherit"
          aria-label="toggle dark mode"
        >
          {mode === "dark" ? <Brightness7Icon /> : <Brightness4Icon />}
        </IconButton>
      </Box>

      <Typography
        variant="body2"
        color="text.secondary"
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 1,
        }}
      >
        Built by Francesc Jordi Sacco & Theodor Vavassori -{" "}
        <Link
          href="https://github.com/sccjrd/ir-project"
          target="_blank"
          rel="noopener noreferrer"
          sx={{ display: "inline-flex", alignItems: "center" }}
        >
          <img
            src={
              mode === "dark" ? "./github-mark-white.svg" : "./github-mark.svg"
            }
            alt="GitHub repository"
            style={{ width: 20, height: 20 }}
          />
        </Link>
      </Typography>
    </Box>
  );
}

export default Footer;
