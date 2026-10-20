import React, { useEffect, useRef } from 'react'
import { useState } from 'react'
import "./AIAssistance.css"
import { useParams } from 'react-router-dom';
import { useAIProvider } from '../context/AIProviderContext';

function AIAssistance() {
    const chatRef = useRef(null);
    const params = useParams()
    const {id} = params;
    const provider = localStorage.getItem("ai_provider");
    if (!provider) {
  setMessages((prev) => [
    ...prev,
    {
      role: "AI",
      content: "Please select an AI provider in Settings first.",
    },
  ]);
  return;
}


    const [messages,setMessages] = useState([]);
    const [input,setInput] = useState("");
    const [isLoading,setLoading] = useState(false);

    useEffect(()=>{
        function handleExplainSelection(event){
            const selectedText = event.detail.text;
            console.log(event)

            addMessage(`Explain this selected text from my PDF:\n\n"${selectedText}"`);
        }
        window.addEventListener("studyos:explain-selection",handleExplainSelection);
        return ()=>{
            window.removeEventListener("studyos:explain-selection",handleExplainSelection);
        }
    },[]);

    async function addMessage(message){
        const question = message.trim()

        if(!question || isLoading) return;
        setLoading(true);

        setMessages(prevMessages => [...prevMessages,{role:"User",content:question},{role:"AI",content : ""}]);
        setInput("");
  try {
        const response = await fetch(
  `http://localhost:8000/ai/chat?api=${encodeURIComponent(provider)}`,
  {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials:"include",
            body: JSON.stringify({
                question: question,
                document_id: id,
                page_number : 0,




            })
        });

        if (!response.ok) {
                const errorDetails = await response.text();
                console.error("Backend error:", errorDetails);
            throw new Error(`HTTP error: ${response.status}`);
        }
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while(true){
            const {value,done} = await reader.read();
            
            if (done) break;

            const chunk = decoder.decode(value,{stream:true});

        

  
        setMessages(prevMessages => {
            const updated = [...prevMessages];
            const lastIndex = updated.length - 1;

            updated[lastIndex] = {...updated[lastIndex],content : updated[lastIndex].content + chunk};
            return updated;
        });
    }
    
    const remaining  = decoder.decode();


    if (remaining) {
        setMessages(prevMessages => {
            const updated = [...prevMessages];
            const lastIndex = updated.length - 1;

            updated[lastIndex] = {
                ...updated[lastIndex],
                content: updated[lastIndex].content + remaining
            };

            return updated;
        });
    }
}
    catch(error){
        console.error("AI request failed",error);
           setMessages(prev => {
            const updated = [...prev];
            const lastIndex = updated.length - 1;

            updated[lastIndex] = {
                ...updated[lastIndex],
                content: "Failed to get an AI response. Check the backend and try again."
            };

            return updated;
        });

    }
    finally{
        setLoading(false);
    }
    

   
    }

    function sendMessage(e){
        e.preventDefault();
        if(!input.trim()) return;
        addMessage(input);
    }
    function handleAction(action){
        addMessage(action)
        console.log("handle running");
        
    }
useEffect(() => {
    if (chatRef.current) {
        chatRef.current.scrollTop =
            chatRef.current.scrollHeight;
    }
}, [messages,isLoading]);
  return (  
    <div className="ai-assistance">
    <div className="suggested-actions">
        <button onClick={()=>handleAction("Explain this page")} disabled={isLoading}>Explain this page</button>
        <button onClick={()=>handleAction("Summerize")} disabled={isLoading}>Summerize this topic</button>
        <button onClick={()=>handleAction("Quiz me ")} disabled={isLoading}>Quiz me on this section</button>
    </div>
    <div className="chatbox" ref={chatRef} >{messages.map((message,index)=>(<p key={index}><strong>{message.role}:</strong>{message.content}</p>))}
             {isLoading && <p>AI is thinking....</p>}
             </div>
        

    
    <div>
         <form className='chat-input' onSubmit={sendMessage}>
       <input value={input} onChange={(e)=>setInput(e.target.value)} placeholder='Ask something...'></input>
        <button className="send_button" type="submit" disabled={isLoading}>Send</button>
        </form>
       
    </div>
    </div>
  )
}

export default AIAssistance