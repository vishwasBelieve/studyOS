import "./Navbar.css";
export default function Navbar(props) {
  
  return (
    <header className="navbar">
      <nav className="navbar-container">
        <button className="navbar-menu-btn" aria-label="Open menu" onClick={props.toggleSidebar}>
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