import { useEffect, useState } from "react";

export default function App() {
  const [health, setHealth] = useState(null);
  const base = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

  useEffect(() => {
    fetch(`${base}/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: "backend_not_reachable" }));
  }, [base]);

  return (
    <div style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>AI Learning Agent</h1>
      <p>Home page (frontend tối thiểu).</p>

      <h2>Backend health</h2>
      <pre>{JSON.stringify(health, null, 2)}</pre>
    </div>
  );
}
