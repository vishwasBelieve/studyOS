import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Singup.css";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : "Signup failed. Please check your details."
        );
      }

      navigate("/login");
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <main className="auth-shell">
        <section className="reading-side">
          <div className="reading-content">
            <p className="eyebrow">BETWEEN PAGES</p>
            <h1>Your reading desk.</h1>
            <p className="reading-description">
              Keep your documents, notes, and ideas in one quiet place.
            </p>

            <div className="quote">
              <span className="quote-mark">“</span>
              <p>
                A good book is a conversation between the reader and the page.
              </p>
            </div>
          </div>
        </section>

        <section className="account-side">
          <div className="form-wrap">
            <div className="form-header">
              <p className="eyebrow">GET STARTED</p>
              <h2>Create your account</h2>
              <p>Set up your reading desk.</p>
            </div>

            <form className="auth-form" onSubmit={handleSubmit}>
              <div className="field">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="field">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  placeholder="Create a password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              {error && <p role="alert">{error}</p>}

              <button
                type="submit"
                className="submit-button"
                disabled={loading}
              >
                {loading ? "Creating account..." : "Sign up"}
              </button>
            </form>

            <p className="form-footer">
              Already have an account?{" "}
              <button
                type="button"
                className="signup-link"
                onClick={() => navigate("/login")}
              >
                Sign in
              </button>
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}