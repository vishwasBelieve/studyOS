import React, { useEffect, useRef } from 'react'
import { useState } from 'react'
import "./AiAssistance.css"
function AiAssistance() {
    const chatRef = useRef(null);

    const [messages,setMessages] = useState([]);
    const [input,setInput] = useState("");
    const [isLoading,setLoading] = useState(false);

    function addMessage(message){
        setMessages(prevMessages => [...prevMessages,{role:"User",content:message},]);
        setLoading(true)
        setTimeout(()=>{
            setMessages(prevMessages =>[...prevMessages,{role:"AI",content:"This is temporary AI response"}]);
            setLoading(false);

        },2000)
        setInput("");
    }

    function sendMessage(){
        if(!input.trim()) return;
        addMessage(input);
    }
    function handleAction(action){
        addMessage(action)
        
    }
useEffect(() => {
    if (chatRef.current) {
        chatRef.current.scrollTop =
            chatRef.current.scrollHeight;
    }
}, [messages,isLoading]);
  return (  
    <>
    <div className="ai-assistance">
    <div className="suggested-actions">
        <button onClick={()=>handleAction("Explain this page")} disabled={isLoading}>Explain this page</button>
        <button onClick={()=>handleAction("Summerize")} disabled={isLoading}>Summerize this topic</button>
        <button onClick={()=>handleAction("Quiz me ")} disabled={isLoading}>Quiz me on this section</button>
    </div>
    <div className="chatbox" ref={chatRef} >{messages.map((message,index)=>(<p key={index}><strong>{message.role}:</strong>{message.content}</p>))}
             {isLoading && <p>AI is thinking....</p>}
             </div>
        

    </div>
    <div className="chat-input">
        <input value={input} onChange={(e)=>setInput(e.target.value)} placeholder='Ask something...'></input>
        <button onClick={sendMessage } disabled={isLoading}>Send</button>
       
    </div>
    </>
  )
}

export default AiAssistance