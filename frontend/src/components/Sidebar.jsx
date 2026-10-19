import "./Sidebar.css"
import { useAuth } from "../context/AuthContext"
import { Link } from "react-router-dom"


export default function Sidebar(){
  const {logout} = useAuth()
    return ( <aside className="sidebar">
      <ul className="sidebar-list">
        <li><a href="#">Recent documents</a></li>
        <li><a href="#">Upload</a></li>
        <li><a href="#">Notes</a></li>
        <li><Link to="/settings">Settings</Link></li>
        <li><button type="button" onClick={logout}>Logout</button></li>
      </ul>
    </aside>)
}