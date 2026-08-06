import {createRoot} from "react-dom/client"
import { StrictMode } from "react"
import App from "./App.jsx"
import "./index.css"
import { RouterProvider } from "react-router-dom"
import router from "./router.jsx"
const root = createRoot(document.getElementById("root"))


root.render(<StrictMode><RouterProvider router={router}/></StrictMode>)