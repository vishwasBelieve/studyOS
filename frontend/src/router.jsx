import { createBrowserRouter } from "react-router-dom";
import Mainlayout from "./layouts/Mainlayout.jsx"
import DocumentPage from "./pages/DocumentPage"
import Dashboard  from "./pages/Dashboard.jsx";

const router = createBrowserRouter([
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