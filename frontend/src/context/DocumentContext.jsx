import {useState} from "react-dom"

const [documents,setDocuments] = useState([

]);

function uploadFunction(file){
    console.log("Upload button was clicked");
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