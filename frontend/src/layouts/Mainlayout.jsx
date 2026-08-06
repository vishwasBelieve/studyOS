import Sidebar from "../components/Sidebar.jsx";
import Dashboard from "../pages/Dashboard.jsx";
import { Outlet } from "react-router-dom";
import "./Mainlayout.css";
import {useState} from "react"



export default function MainLayout() {


    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard docArray = {documents} uploadFunc = {uploadFunction} onDelete ={deleteDocument}/>
            <Outlet/>
        </main>
    );
}