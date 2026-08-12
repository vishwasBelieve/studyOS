import { useContext } from "react"
import {FaTrash} from "react-icons/fa"
import { Link, useOutletContext } from "react-router-dom"
export default  function DocumentCard(props){

    const {closeSidebar} = useOutletContext()
    
    

    return (<>
        <p>{props.document.id}</p>
        <p ><Link to={`/document/${props.document.id}`} onClick={closeSidebar}>{props.document.name}</Link></p>
        <p> {props.document.page} pages</p>
        <button onClick ={()=>  props.onDelete(props.document.id)}><FaTrash/></button>
        </>
    )
}