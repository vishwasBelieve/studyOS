import Navbar from "./components/Navbar.jsx"
import MainLayout from "./layouts/Mainlayout";
import "./app.css";




export default function App() {

  return (
    <div className="app">
      <Navbar />
      <MainLayout />
    </div>
  );
}