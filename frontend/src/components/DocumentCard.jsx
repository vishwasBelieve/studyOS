import {FaTrash} from "react-icons/fa"

export default  function DocumentCard(props){

    function handleDelete(){
        
        
    }

    console.log(props)
    return (<><p>{props.name}</p>
        <p> {props.page} pages</p>
        <button onClick={handleDelete}><FaTrash/></button>
        </>
    )
}