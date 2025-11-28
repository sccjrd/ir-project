import { useState } from "react";
import {
  Box,
  Button,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

function SearchTags({ categories }) {
  const [expanded, setExpanded] = useState(false);

  const handleChange = (_event, isExpanded) => {
    setExpanded(isExpanded);
  };

  return (
    <Accordion
      expanded={expanded}
      onChange={handleChange}
      sx={{ mt: 1.5, boxShadow: "none" }}
    >
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 500 }}>
          Show tags
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
          {categories.map((tag) => (
            <Button
              key={tag}
              size="small"
              variant="outlined"
              disableElevation
              sx={{
                borderRadius: "999px",
                textTransform: "uppercase",
                fontWeight: 500,
                letterSpacing: 0.5,
                paddingX: 1.5,
              }}
            >
              {tag}
            </Button>
          ))}
        </Box>
      </AccordionDetails>
    </Accordion>
  );
}

export default SearchTags;
