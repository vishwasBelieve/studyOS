import Sidebar from "./Sidebar";
import Dashboard from "./Dashboard";
import "./mainlayout.css";

export default function MainLayout() {
    return (
        <main className="main-layout">
            <Sidebar />
            <Dashboard />
        </main>
    );
}