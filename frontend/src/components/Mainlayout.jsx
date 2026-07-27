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
function uploadFunction(){
    console.log("Upload button was clicked");
    setDocuments(prevDocument=>[...prevDocument,{  
    id: 4,
    name: "New Document",
    pages: 1,
  }])
}

    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard docArray = {documents} uploadFunc = {uploadFunction}/>
        </main>
    );
}