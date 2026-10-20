import { useState } from "react";
import "./Settings.css"
import AISettings from "../components/AISettings";

export default function Settings(){
     const [provider,setProvider] = useState("openai");
     const[apiKey,setApiKey] = useState("");

    async  function handleSave(e){
        e.preventDefault();

        try{
            const reponse = await fetch("http://localhost:8000/settings/ai_keys",
                {method:"PUT",
                    headers:{
                        "Content-Type":"application/json",
                    },
                    credentials:"include",
                    body:JSON.stringify({
                        provider,
                        api_key:apiKey,
                    })
                }
            );
            if(!reponse.ok){
                throw new Error("Failed to save settings");
            }
            setApiKey("");
            alert("Setting saved successfully")

        }catch(error){
            alert(error.message);
        }
     }
    return (
       <main className="settings-page">
  <h1>AI Settings</h1>
  <p>Configure the AI provider you want StudyOS to use.</p>

  <section className="settings-card">
            <h2>AI Provider</h2>
            <p className="card-description">
            Choose the model provider for your study sessions.
            </p>

            <form className="settings-form" onSubmit={handleSave}>
            <div className="settings-field">
                <label htmlFor="provider">AI Provider</label>
                <select
        id="provider"
        value={provider}
        onChange={(e) => setProvider(e.target.value)}
        >
  <option value="openai">OpenAI</option>
  <option value="anthropic">Anthropic</option>
  <option value="google">Google Gemini</option>
</select>
      </div>

      <div className="settings-field">
        <label htmlFor="apiKey">API Key</label>
                <input
            id="apiKey"
            type="password"
            placeholder="Enter your API key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            />
        <p className="field-help">
          Your provider may charge you for API usage.
        </p>
      </div>

      <div className="settings-notice">
        <p>
          Use an API key from a provider you trust.
          Your key should be handled securely by the backend.
        </p>
      </div>

      <div className="settings-actions">
        <button className="settings-save-button" type="submit">
          Save Settings
        </button>
      </div>
    </form>
  </section>
  <AISettings/>
</main>
    )
}