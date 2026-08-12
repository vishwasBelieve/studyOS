import { createContext } from "react";
import { useState } from "react";
export const DocumentContext = createContext()


export function DocumentProvider(props){
    const [documents , setDocuments] = useState([])
    
    function uploadDocument(file){
    setDocuments(prevDocuments=>[...prevDocuments,{
        id : crypto.randomUUID(),
        name : file.name,
        pages : "__",
        file : file 
    }])
}
    function deleteDocument(id){
    setDocuments(prevDocuments=>prevDocuments.filter(doc => doc.id !== id))

    }

    
    return (<DocumentContext.Provider value={{documents,uploadDocument,deleteDocument}}>
        {props.children}
    </DocumentContext.Provider>)
}










