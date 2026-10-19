import React from 'react'
import { DocumentContext } from '../context/DocumentContext'
import { useContext } from 'react'
import { useParams } from 'react-router-dom'
import "./DocumentHeader.css"

function DocumentHeader() {
    const parms = useParams()
    const {documents} = useContext(DocumentContext)
    console.log(documents)
    const document = documents.find(doc => doc.id === parms.id)
      return (
    <div className="header">
      {document ? document.name : ""}
    </div>
  )
  }


export default DocumentHeader