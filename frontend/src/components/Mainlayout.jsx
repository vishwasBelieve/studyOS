import Sidebar from "./Sidebar.jsx"
import Dashboard from "./Dashboard"
import "./mainlayout.css"
export default function Mainlyout(){
    return (<main><div className="sidebar"><Sidebar /></div><div className="dashboard"><Dashboard /></div></main>)
}