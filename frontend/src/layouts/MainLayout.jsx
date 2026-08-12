import Sidebar from "../components/Sidebar.jsx";
import Navbar from "../components/Navbar.jsx";
import { Outlet } from "react-router-dom";
import "./MainLayout.css";


export default function MainLayout() {




    return (<>
     <Navbar/>
        <main className="main-layout">
            <Sidebar />
            <Outlet/>
        </main>
    </>);
}