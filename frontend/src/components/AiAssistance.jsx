import React from 'react'
import { useState } from 'react'
function AiAssistance() {

    const [messages,setMessages] = useState([]);
    const [input,setInput] = useState("");

    function addMessage(message){
        setMessages(prevMessages => [...prevMessages,{role:"User",content:message},
            {role:"AI",content:"This is an temporary AI resopnse"}
        ]);
        setInput("");
    }

    function sendMessage(){
        if(!input.trim()) return;
        addMessage(input);
        setInput("");
    }
    function handleAction(action){
        addMessage(action)
        setInput("");
        
    }

  return (  
    <>
    <div className="ai-assistance">
    <div className="suggested-actions">
        <button onClick={()=>handleAction("Explain this page")}>Explain this page</button>
        <button onClick={()=>handleAction("Summerize")}>Summerize this topic</button>
        <button onClick={()=>handleAction("Quiz me ")}>Quiz me on this section</button>
    </div>
    <div>{messages.map((message,index)=>(<p key={index}><strong>{message.role}:</strong>{message.content}</p>))}</div>
    </div>
    <div className="chat-input">
        <input value={input} onChange={(e)=>setInput(e.target.value)} placeholder='Ask something...'></input>
        <button onClick={sendMessage}>Send</button>
    </div>
    </>
  )
}

export default AiAssistance