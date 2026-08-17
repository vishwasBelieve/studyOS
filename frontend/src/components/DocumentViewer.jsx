import { useParams } from "react-router-dom"
import { useState, useContext, useEffect } from "react"
import { DocumentContext } from "../context/DocumentContext"
import "./DocumentViewer.css"

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
    <div className="document-viewer">
        {fileUrl && (<iframe
            src ={fileUrl} title={document.name}></iframe>)}
            </div>
    )
}