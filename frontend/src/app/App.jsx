import SearchPage from "../features/search/components/SearchPage.jsx";
import Footer from "../shared/components/Footer.jsx";

function App({ toggleColorMode, mode }) {
  return (
    <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
      <div style={{ flex: 1 }}>
        <SearchPage />
      </div>
      <Footer toggleColorMode={toggleColorMode} mode={mode} />
    </div>
  );
}

export default App;
