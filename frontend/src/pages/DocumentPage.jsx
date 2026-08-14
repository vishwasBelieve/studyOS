import { useParams } from "react-router-dom"
import { useState, useContext, useEffect } from "react"
import { DocumentContext } from "../context/DocumentContext"
import DocumentViewer from "../components/DoicumentViewer"
import DocumentHeader from "../components/DocumentHeader"
import AiAssistance from "../components/AiAssistance"
import "./DocumentPage.css"


export default function DocumentPage(){
    return (
    <div className="document-page">
        <DocumentHeader/>
        <div className="workspace">
        <DocumentViewer/>
        <AiAssistance/>
        </div>
        </div>)
}