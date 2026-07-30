import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";
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
    console.log("Delete button is clicked")
    console.log(id)
    setDocuments(prevDocuments=>prevDocuments.filter(doc => doc.id !== id))
}

    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard docArray = {documents} uploadFunc = {uploadFunction} onDelete ={deleteDocument}/>
        </main>
    );
}