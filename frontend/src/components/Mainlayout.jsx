import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";
import "./Mainlayout.css";
import {useState} from "react"



export default function MainLayout() {
    const [documents,setDocuments] = useState([
//   {
//     id: 1,
//     name: "Operating Systems.pdf",
//     pages: 320,
//   },
//   {
//     id: 2,
//     name: "DBMS Notes.pdf",
//     pages: 145,
//   },
]);
function uploadFunction(file){
    console.log("Upload button was clicked");
    setDocuments(prevDocument=>[...prevDocument,{id : Date.now(),
        name : file.name,
        pages : "__"
    }])
}

    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard docArray = {documents} uploadFunc = {uploadFunction}/>
        </main>
    );
}