import {FaTrash} from "react-icons/fa"

export default  function DocumentCard(props){

    function handleDelete(){
        
        
    }
    return (<>
        <p>{props.document.id}</p>
        <p>{props.document.name}</p>
        <p> {props.document.page} pages</p>
        <button onClick ={()=>  props.onDelete(props.document.id)}><FaTrash/></button>
        </>
    )
}