import { createBrowserRouter,Navigate} from "react-router-dom";
import Mainlayout from "./layouts/MainLayout.jsx"
import DocumentPage from "./pages/DocumentPage"
import Dashboard  from "./pages/Dashboard.jsx";
import Login from "./pages/Login.jsx";
import ProtectedRoute from "./components/ProtectedRouter.jsx";
import Settings from "./pages/Settings.jsx";
const router = createBrowserRouter([
    {path:"/login",element:<Login/>},
    {element:<ProtectedRoute/>,
        children:[ 
            {path : "/",
        element: <Mainlayout/>,
        children : [
            {index:true,element:<Navigate to="/login" replace/>},
            {path: "/settings",element:<Settings/>},
            {path: "/dashboard", element : <Dashboard/>},
            {
                path: "document/:id",element : <DocumentPage/>
            }

        ]
    }]
}]);

export default router;