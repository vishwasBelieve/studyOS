import "./Navbar.css";
import { Link } from "react-router-dom";
export default function Navbar(props) {
  
  return (
    <header className="navbar">
      <nav className="navbar-container">
        <button className="navbar-menu-btn" aria-label="Open menu" onClick={props.toggleSidebar}>
          <span className="hamburger">☰</span>
        </button>
        
        <Link to="/dashboard" className="navbar-brand">StudyOS</Link>
        
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