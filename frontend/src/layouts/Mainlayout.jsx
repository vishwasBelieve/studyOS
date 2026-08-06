import Sidebar from "../components/Sidebar.jsx";
import Dashboard from "../pages/Dashboard.jsx";
import { Outlet } from "react-router-dom";
import "./Mainlayout.css";
import {useState} from "react"



export default function MainLayout() {
    const [documents,setDocuments] = useState([

]);
function uploadFunction(file){
    console.log("Upload button was clicked");
    setDocuments(prevDocuments=>[...prevDocuments,{
        id : crypto.randomUUID(),
        name : file.name,
        pages : "__",
        file : file
    }])
}

function deleteDocument(id){
    setDocuments(prevDocuments=>prevDocuments.filter(doc => doc.id !== id))
}

    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard docArray = {documents} uploadFunc = {uploadFunction} onDelete ={deleteDocument}/>
            <Outlet/>
        </main>
    );
}