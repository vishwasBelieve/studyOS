import { useParams } from "react-router-dom"
import { useState, useContext, useEffect } from "react"
import { DocumentContext } from "../context/DocumentContext"

export default function DocumentViewer(){
    const parms = useParams()
    const {documents} = useContext(DocumentContext)
    const document = documents.find(doc => doc.id === parms.id)
    const [fileUrl,setFileUrl] = useState(null);

    useEffect(()=>{
        if(!document) return;
        const url = URL.createObjectURL(document.file);
        setFileUrl(url);
        return () =>{
            URL.revokeObjectURL(url);
        }
    },[document])

    if(!document){
        return (<h1>Document not found</h1>)
    }

    return (
    <div>
        <h1>{document?.name}</h1>
        {fileUrl && (<iframe
            src ={fileUrl} width = "100%" height ="700px" title={document.name}></iframe>)}
            </div>
    )
}