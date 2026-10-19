
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { fetchPdf } from "../api";
import "./DocumentViewer.css";

export default function DocumentViewer() {
  const { id } = useParams();

  const [fileUrl, setFileUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
    <div className="document-viewer">
      {fileUrl && <iframe src={fileUrl} title="PDF viewer" />}
    </div>
  );
}
