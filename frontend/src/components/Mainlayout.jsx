import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";
import "./mainlayout.css";

const documents = [
  {
    id: 1,
    name: "Operating Systems.pdf",
  },
  {
    id: 2,
    name: "DBMS Notes.pdf",
  },
];
export default function MainLayout() {
    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard docArray = {documents}/>
        </main>
    );
}