import { useParams } from "react-router-dom"
import { useState, useContext, useEffect } from "react"
import { DocumentContext } from "../context/DocumentContext"
import DocumentViewer from "../components/DocumentViewer"
import DocumentHeader from "../components/DocumentHeader"
import AiAssistance from "../components/AiAssistance"
import "./DocumentPage.css"


export default function DocumentPage(){

    const [aiOpen,setAiOpen] = useState(true)
    function aiOpenORNot(){
        setAiOpen(prev=>!prev)
    }

    return (
    <div className="document-page">
        <DocumentHeader/>
        <div className={`workspace ${aiOpen?"ai-open" : "ai-closed"}`}>
        <DocumentViewer/>
        {aiOpen && <AiAssistance/>}
        </div>
       <button 
                    className="Ai-button" 
                    onClick={() => setAiOpen(prev => !prev)}
                >{aiOpen?"X":"AI"}</button>
    </div>)
}