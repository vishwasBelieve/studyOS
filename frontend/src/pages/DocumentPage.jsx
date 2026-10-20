
import { useState } from "react";
import DocumentViewer from "../components/DocumentViewer";
import DocumentHeader from "../components/DocumentHeader";
import AIAssistance from "../components/AIAssistance";
import "./DocumentPage.css";

export default function DocumentPage() {
    const [aiOpen, setAiOpen] = useState(true);

    return (
        <div className="document-page">
            <DocumentHeader />

            <div className={`workspace ${aiOpen ? "ai-open" : "ai-closed"}`}>
                <DocumentViewer />

                <div className={`ai-panel ${aiOpen ? "ai-visible" : "ai-hidden"}`}>
                    <AIAssistance />
                </div>
            </div>

            <button
                className="Ai-button"
                onClick={() => setAiOpen(prev => !prev)}
            >
                {aiOpen ? "X" : "AI"}
            </button>
        </div>
    );
}
