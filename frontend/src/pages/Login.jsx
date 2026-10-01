
import "./Login.css";

export default function Login() {
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
              <p className="eyebrow">WELCOME BACK</p>
              <h2>Sign in to your account</h2>
              <p>Continue where you left off.</p>
            </div>

            <div className="tabs">
              <input
                type="radio"
                id="login-tab"
                name="auth-tab"
                defaultChecked
              />
              <label htmlFor="login-tab">Login</label>

              <input
                type="radio"
                id="signup-tab"
                name="auth-tab"
              />
              <label htmlFor="signup-tab">Sign up</label>
            </div>

            <form className="auth-form">
              <div className="field">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  placeholder="you@example.com"
                />
              </div>

              <div className="field">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  placeholder="Your password"
                />
              </div>

              <button type="submit" className="submit-button">
                Sign in
              </button>
            </form>

            <p className="form-footer">
              Your documents are waiting for you.
            </p>

          </div>
        </section>

      </main>
    </div>
  );
}

