import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";
import "./Mainlayout.css";


const documents = [
  // {
  //   id: 1,
  //   name: "Operating Systems.pdf",
  //   pages: 320,
  // },
  // {
  //   id: 2,
  //   name: "DBMS Notes.pdf",
  //   pages: 145,
  // },
];

export default function MainLayout() {
    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard docArray = {documents}/>
        </main>
    );
}