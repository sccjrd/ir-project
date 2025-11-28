import { Paper, Box, Typography, Link as MuiLink } from "@mui/material";
import SimilarHacksAccordion from "./SimilarHacksAccordion";
import SearchTags from "./SearchTags";

/** Highlight occurrences of `query` inside `text` using <mark>. */
function highlightText(text, query) {
  if (!text || !query) return text;

  const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${escaped})`, "gi");
  const parts = text.split(regex);

  return parts.map((part, idx) =>
    idx % 2 === 1 ? (
      <mark key={idx} style={{ backgroundColor: "#fff59d" }}>
        {part}
      </mark>
    ) : (
      part
    )
  );
}

/** Build a snippet centered around the first occurrence of the query. */
function buildSnippet(result, query) {
  const fullText =
    result?.content || result?.excerpt || "No description available yet.";

  const SNIPPET_LENGTH = 260;

  if (!fullText) return "";

  if (!query) {
    return fullText.length > SNIPPET_LENGTH
      ? fullText.slice(0, SNIPPET_LENGTH) + "…"
      : fullText;
  }

  const lowerText = fullText.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const idx = lowerText.indexOf(lowerQuery);

  if (idx === -1) {
    return fullText.length > SNIPPET_LENGTH
      ? fullText.slice(0, SNIPPET_LENGTH) + "…"
      : fullText;
  }

  const CONTEXT_BEFORE = 80;
  let start = Math.max(idx - CONTEXT_BEFORE, 0);
  let end = start + SNIPPET_LENGTH;

  if (end > fullText.length) {
    end = fullText.length;
    start = Math.max(end - SNIPPET_LENGTH, 0);
  }

  let snippet = fullText.slice(start, end).trim();

  if (start > 0) snippet = "…" + snippet;
  if (end < fullText.length) snippet = snippet + "…";

  return snippet;
}

function SearchResultCard({ result, query }) {
  const snippet = buildSnippet(result, query);
  const dateStr =
    typeof result.date === "string"
      ? result.date.slice(0, 10)
      : result.date
      ? String(result.date).slice(0, 10)
      : "";

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        borderRadius: 2,
        "&:hover": { boxShadow: 2 },
      }}
    >
      <Box>
        {/* URL + source line */}
        <Typography variant="caption" color="text.secondary">
          {result.source && `${result.source} · `}
          {result.url}
        </Typography>

        {/* Title */}
        <Typography
          variant="h6"
          component={MuiLink}
          href={result.url}
          target="_blank"
          rel="noopener noreferrer"
          underline="hover"
          sx={{ display: "block", mt: 0.5 }}
        >
          {highlightText(result.title || "Untitled hack", query)}
        </Typography>
        {/* {console.log(result)} */}
        {/* Snippet */}
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            mt: 0.5,
            display: "-webkit-box",
            WebkitLineClamp: 3,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
          }}
        >
          {highlightText(snippet, query)}
        </Typography>

        {/* Meta line */}
        <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
          {result.author && `${result.author} · `}
          {dateStr}
        </Typography>

        {/* Search query tags */}
        <SearchTags categories={result.categories} />

        {/* Similar hacks accordion */}
        <SimilarHacksAccordion hackId={result.id} />
      </Box>
    </Paper>
  );
}

export default SearchResultCard;
