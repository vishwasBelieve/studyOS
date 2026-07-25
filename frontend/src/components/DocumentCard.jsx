export default  function DocumentCard(props){
    console.log(props)
    return (<><p>{props.name}</p>
        <p> {props.page} pages</p>
        </>
    )
}