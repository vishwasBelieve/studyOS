import Navbar from "./components/Navbar.jsx"
import MainLayout from "./layouts/MainLayout.jsx";
import "./app.css";
import Login from "./pages/Login.jsx";




export default function App() {

  return (
    <div className="app">
      {/* <Navbar />
      <MainLayout /> */}
      <Login/>
    </div>
  );
}