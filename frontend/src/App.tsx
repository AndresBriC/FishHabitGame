import { useEffect, useState } from "react";

import { getHealth } from "./api/client";
import "./App.css";

type ApiStatus = "checking" | "available" | "unavailable";

function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>("checking");

  useEffect(() => {
    void getHealth()
      .then(() => setApiStatus("available"))
      .catch(() => setApiStatus("unavailable"));
  }, []);

  return (
    <main className="app-shell">
      <section className="welcome-card" aria-labelledby="page-title">
        <p className="eyebrow">Fish Habit Game</p>
        <h1 id="page-title">Build positive habits. Collect cool fish.</h1>
        <p className="intro">
          The web application foundation is ready. Registration, today&apos;s
          pond, and your collection are the next features.
        </p>
        <p className={`api-status api-status--${apiStatus}`} role="status">
          API status: {apiStatus}
        </p>
      </section>
    </main>
  );
}

export default App;
