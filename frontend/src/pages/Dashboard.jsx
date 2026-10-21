
import "./Dashboard.css";
import DocumentCard from "../components/DocumentCard.jsx";
import { useContext, useRef, useState } from "react";
import { DocumentContext } from "../context/DocumentContext.jsx";

export default function Dashboard() {
  const { documents, uploadDocument, deleteDocument } =
    useContext(DocumentContext);

  const [isProcessing, setIsProcessing] = useState(false);
  const pickerRef = useRef(null);

  const documentElements = documents.map((doc) => (
    <DocumentCard
      key={doc.id}
      document={doc}
      onDelete={deleteDocument}
    />
  ));

  function pickerFunction() {
    pickerRef.current?.click();
  }

  async function handleChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    setIsProcessing(true);

    try {
      await uploadDocument(file);
    } catch (error) {
      console.error("Document upload failed:", error);
    } finally {
      setIsProcessing(false);
      e.target.value = "";
    }
  }

  return (
    <div className="dashboard">
      <input
        ref={pickerRef}
        type="file"
        accept="application/pdf"
        style={{ display: "none" }}
        onChange={handleChange}
      />

      {isProcessing && (
        <div className="processing-status">
          <span className="spinner" />
          <span>Uploading and processing document...</span>
        </div>
      )}

      {documentElements.length === 0 ? (
        <div className="empty-state">
          <svg
            className="empty-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.5"
          >
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="12" y1="18" x2="12" y2="18" />
            <line x1="9" y1="15" x2="15" y2="15" />
          </svg>

          <h2>No documents yet</h2>
          <p>Upload a document to get started.</p>

          <button
            className="upload-btn"
            onClick={pickerFunction}
            disabled={isProcessing}
          >
            Upload Document
          </button>
        </div>
      ) : (
        <div className="nonEmpty-state">
          {documentElements}

          <button
            className="upload-btn"
            onClick={pickerFunction}
            disabled={isProcessing}
          >
            Upload document
          </button>
        </div>
      )}
    </div>
  );
}
