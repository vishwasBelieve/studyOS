import "./Dashboard.css";
import {useState} from "react";


export default function Dashboard(props){
  const documentElements = props.docArray.map(doc=>{return <h1 key = {doc.id}>{doc.name}</h1>})

  if(documentElements.length === 0){
    return (<div className="dashboard">
      <div className="empty-state">
        <svg className="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="12" y1="18" x2="12" y2="18" />
          <line x1="9" y1="15" x2="15" y2="15" />
        </svg>
        <h2>No documents yet</h2>
        <p>Upload a document to get started.</p>
        <button className="upload-btn">Upload Document</button>
      </div>
    </div>)
  }

  else {
    return <h1>{documentElements}</h1>
  }
}