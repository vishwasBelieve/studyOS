import { createContext, useState } from "react";
import { uploadPdf } from "../api";
export const DocumentContext = createContext()


export function DocumentProvider(props){
    const [documents , setDocuments] = useState([])
    
    async function uploadDocument(file){
        try{
             const uploadedDocument = await uploadPdf(file);

             setDocuments((prevDocuments)=>[...prevDocuments,{
                ...uploadedDocument,id:uploadedDocument.id,name:uploadedDocument.name,
             }])
          alert("Document uploaded successfully!");    
        }
        catch(error){   
            console.error(error);
            alert(error.message)
    }

    }


    function deleteDocument(id){
    setDocuments(prevDocuments=>prevDocuments.filter(doc => doc.id !== id))

    }

    return (<DocumentContext.Provider value={{documents,uploadDocument,deleteDocument}}>
        {props.children}
    </DocumentContext.Provider>)
}










