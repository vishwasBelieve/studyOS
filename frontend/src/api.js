const API_BASE_URL = "http://localhost:8000";

export async function  uploadPdf(file,option={}){
    const formData = new FormData();
    formData.append("file",file);

    const response = await fetch(`${API_BASE_URL}/documents/`,{
        method:"POST",
        credentials : "include",
        body:formData,
        ...option,
    });
    if(response.status == 401){
        window.dispatchEvent(new Event("auth:session-expired"));
    }
    if(!response.ok){
        const error = await response.text()
        throw new Error(`Upload failed (${response.status}): ${error}`)

    }
    return response.json(); 
}

export async function fetchPdf(docId,option={}){
    console.log("fecthing pdf is working...")
        const response = await fetch(`${API_BASE_URL}/documents/${docId}/file`,{
            method:"GET",
            credentials:"include",
            ...option
        });
        if(response.status == 401){
            window.dispatchEvent(new Event("auth:session-expired"));
        }
        if(!response.ok) {
            throw new Error(`PDF fetch failed (${response.status})`);
        }
        const blob = await response.blob();
        return URL.createObjectURL(blob);
}

