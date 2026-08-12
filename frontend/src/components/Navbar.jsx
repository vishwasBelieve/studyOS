import "./Navbar.css";
export default function Navbar() {
  return (
    <header className="navbar">
      <nav className="navbar-container">
        <button className="navbar-menu-btn" aria-label="Open menu">
          <span className="hamburger">☰</span>
        </button>
        
        <a href="/" className="navbar-brand">StudyOS</a>
        
        <form className="navbar-search" role="search">
          <input 
            type="search" 
            placeholder="Search..." 
            aria-label="Search"
          />
        </form>
      </nav>
    </header>
  );
}