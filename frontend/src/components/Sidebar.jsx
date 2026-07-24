import "./sidebar.css"
export default function Sidebar(){
    return ( <aside className="sidebar">
      <ul className="sidebar-list">
        <li><a href="#">Recent documents</a></li>
        <li><a href="#">Upload</a></li>
        <li><a href="#">Notes</a></li>
        <li><a href="#">Settings</a></li>
      </ul>
    </aside>)
}