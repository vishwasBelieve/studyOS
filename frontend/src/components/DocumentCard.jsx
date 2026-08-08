import {FaTrash} from "react-icons/fa"
import { Link } from "react-router-dom"
export default  function DocumentCard(props){
    

    return (<>
        <p>{props.document.id}</p>
        <p><Link to={`/document/${props.document.id}`}>{props.document.name}</Link></p>
        <p> {props.document.page} pages</p>
        <button onClick ={()=>  props.onDelete(props.document.id)}><FaTrash/></button>
        </>
    )
}