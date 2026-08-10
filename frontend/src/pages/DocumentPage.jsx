import { useParams } from "react-router-dom"
import { useState, useContext, useEffect } from "react"
import { DocumentContext } from "../context/DocumentContext"
import DocumentViewer from "../components/DoicumentViewer"
import DocumentHeader from "../components/DocumentHeader"
import AiAssistance from "../components/AiAssistance"



export default function DocumentPage(){
    return (<>
        <DocumentHeader/>
        <DocumentViewer/>
        <AiAssistance/>
        </>)
}