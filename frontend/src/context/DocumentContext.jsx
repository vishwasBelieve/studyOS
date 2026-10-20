import { createContext, useState ,useEffect} from "react";
import { uploadPdf } from "../api";
import { fetchDocuments } from "../api";
import { useAuth } from "./AuthContext";
export const DocumentContext = createContext()


export function DocumentProvider(props){
    const { user, loading: authLoading } = useAuth();
    const [documents , setDocuments] = useState([])
    useEffect(() => {
        if (authLoading) return;

        if (!user) {
        setDocuments([]);
        return;
        }
        async function loadDocuments() {
            console.log("loading the document")
            try {
                const data = await fetchDocuments();
                setDocuments(data);
            } catch (error) {
                console.error("Failed to load documents:", error);
            }
        }

        loadDocuments();
    }, [user,authLoading]);


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










