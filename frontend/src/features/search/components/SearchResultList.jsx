import { Stack, Typography } from "@mui/material";
import SearchResultCard from "./SearchResultCard.jsx";

function SearchResultList({
  results,
  query,
  loading,
  onCategorySearch,
  hasSearched,
}) {
  if (!loading && results.length === 0 && query && hasSearched) {
    return (
      <Typography variant="body2" color="text.secondary">
        No results found. Try a different query.
      </Typography>
    );
  }

  if (!loading && results.length === 0 && query && !hasSearched) {
    return (
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ textAlign: "center", mt: 4 }}
      >
        Type your favourite IKEA product and press Enter to give it a new file!
      </Typography>
    );
  }

  return (
    <>
      <Stack spacing={2}>
        {results.map((res) => (
          <SearchResultCard
            key={res.id || res.url}
            result={res}
            query={query}
            onCategorySearch={onCategorySearch}
          />
        ))}
      </Stack>
    </>
  );
}

export default SearchResultList;
