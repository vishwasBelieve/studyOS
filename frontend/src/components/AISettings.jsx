import { useState } from "react";
import "./AISettings.css";

export default function AISettings() {
  const [provider, setProvider] = useState(
    () => localStorage.getItem("ai_provider") || ""
  );

  function handleProviderChange(event) {
    const selectedProvider = event.target.value;

    setProvider(selectedProvider);
    localStorage.setItem("ai_provider", selectedProvider);

    console.log("Saved provider:", localStorage.getItem("ai_provider"));
  }

  return (
    <div className="ai-settings">
      <h2>AI Provider</h2>

      <label htmlFor="ai-provider">Choose your AI provider</label>

      <select
        id="ai-provider"
        value={provider}
        onChange={handleProviderChange}
      >
        <option value="" disabled>Select a provider</option>
        <option value="google">Google Gemini</option>
        <option value="openai">OpenAI</option>
        <option value="anthropic">Anthropic</option>
      </select>

      <p>Selected provider: {provider || "None selected"}</p>
    </div>
  );
}