import Sidebar from "../components/Sidebar.jsx";
import Dashboard from "../pages/Dashboard.jsx";
import Navbar from "../components/Navbar.jsx";
import { Outlet } from "react-router-dom";
import "./Mainlayout.css";
import {useContext, useState} from "react"
import { DocumentContext } from "../context/DocumentContext.jsx";


export default function MainLayout() {
    const context = useContext(DocumentContext)
    const {documents,uploadDocument,deleteDocument} = context;
    console.log(documents)



    return (<>
     <Navbar/>
        <main className="main-layout">
            <Sidebar />
            <Outlet/>
        </main>
    </>);
}