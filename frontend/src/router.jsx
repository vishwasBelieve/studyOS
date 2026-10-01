import { createBrowserRouter } from "react-router-dom";
import Mainlayout from "./layouts/MainLayout.jsx"
import DocumentPage from "./pages/DocumentPage"
import Dashboard  from "./pages/Dashboard.jsx";
import Login from "./pages/Login.jsx";

const router = createBrowserRouter([
    {path:"/login",element:<Login/>},
    {path : "/",
        element: <Mainlayout/>,
        children : [
            {index : true, element : <Dashboard/>},
            {
                path: "document/:id",element : <DocumentPage/>
            }

        ]
    }
])

export default router;