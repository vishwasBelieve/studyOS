
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { fetchPdf } from "../api";
import "./DocumentViewer.css";
import {Document,Page,pdfjs} from "react-pdf"

import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";
import "./DocumentViewer.css";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();


export default function DocumentViewer() {
  const { id } = useParams();
  const [numPages,setNumPages] = useState(0);

  const [fileUrl, setFileUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selection,setSelection] = useState("");

  function handleTextSelection(){
    const selected = window.getSelection()
    const text = selected?.toString().trim()
    if(!text || selected.isCollapsed){
      setSelection(null);
      return;
    } 
    const range = selected.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    setSelection({
    text,
    top: rect.bottom + 8,
    left: rect.left,
  });
  }

  useEffect(() => {
    let objectUrl;

    async function loadPdf() {
      try {
        setLoading(true);
        setError("");



        objectUrl = await fetchPdf(id);
        setFileUrl(objectUrl);
      } catch (err) {
        console.error(err);
        setError(err.message || "Failed to load PDF.");
      } finally {
        setLoading(false);
      }
    }

    loadPdf();

    return () => {
      if (objectUrl) {
        URL.revokeObjectURL(objectUrl);
      }
    };
  }, [id]);

  if (loading) return <p>Loading PDF...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="document-viewer"
      onMouseUp={handleTextSelection}
    onKeyUp={handleTextSelection}>
      {selection && <button className="selection-explain-button" 
      style={{
              position: "fixed",
          top: selection.top,
          left: selection.left,
          zIndex: 1000,
      }} onMouseDown={(event)=>event.preventDefault()} onClick={()=>{
        window.dispatchEvent(new CustomEvent(
        "studyos:explain-selection",{
          detail :{
            text : selection.text,
          },
        }
      ))
      setSelection(null);}}>
        Explain </button>}
      {fileUrl && (<Document
          file={fileUrl}
          onLoadSuccess={({ numPages }) => setNumPages(numPages)}
          onLoadError={(err) => setError(err.message)}
          loading={<p>Rendering PDF...</p>}
        >{Array.from({ length: numPages }, (_, index) => (
            <Page
              key={index + 1}
              pageNumber={index + 1}
              width={750}
              renderTextLayer
              renderAnnotationLayer
            />
          ))}
      </Document>)
      }
    </div>
  );
}
