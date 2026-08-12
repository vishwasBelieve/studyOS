import Sidebar from "../components/Sidebar.jsx";
import Navbar from "../components/Navbar.jsx";
import { Outlet } from "react-router-dom";
import { useState } from "react";
import "./MainLayout.css";


export default function MainLayout() {

    const [isSidebar,setSidebar] = useState(true);

    function toggleSidebar(){
        setSidebar(prevState =>!prevState)

    }
    function closeSidebar(){
        console.log("closing side bar or not")
        setSidebar(false);
    }



    return (<>
     <Navbar toggleSidebar = {toggleSidebar}/>
        <main className="main-layout">
            {isSidebar?<Sidebar/>:<></>}
            <Outlet context = {{closeSidebar}}/>
        </main>
    </>);
}