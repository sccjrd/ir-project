import { Box, Typography, Link } from "@mui/material";

function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        mt: 6,
        textAlign: "center",
        borderTop: 1,
        borderColor: "divider",
      }}
    >
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
        Built by Francesc Jordi Sacco & Theodor Vavassori -{"  "}
        <Link
          href="https://github.com/sccjrd/IR_Project"
          target="_blank"
          rel="noopener noreferrer"
          sx={{ display: "inline-flex", alignItems: "center" }}
        >
          <img
            src="./github-mark.svg"
            alt="GitHub repository"
            style={{ width: 20, height: 20 }}
          />
        </Link>
      </Typography>
    </Box>
  );
}

export default Footer;
