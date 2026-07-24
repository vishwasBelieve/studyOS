import Navbar from "./components/Navbar";
import MainLayout from "./components/Mainlayout";
import "./app.css";

export default function App() {
  return (
    <div className="app">
      <Navbar />
      <MainLayout />
    </div>
  );
}