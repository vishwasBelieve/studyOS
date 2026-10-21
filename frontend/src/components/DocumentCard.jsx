
import { useState } from "react"
import { FaTrash, FaFilePdf } from "react-icons/fa"
import { Link, useOutletContext } from "react-router-dom"
import "./DocumentCard.css"
import { deleteDocument } from "../api"

export default function DocumentCard({ document, onDelete }) {
    const { closeSidebar } = useOutletContext()
    const [deleting, setDeleting] = useState(false)

    async function handleDelete() {
        if (!window.confirm(`Delete "${document.name}"?`)) return

        try {
            setDeleting(true)
            await deleteDocument(document.id)
            onDelete(document.id)
        } catch (error) {
            alert(error.message || "Failed to delete document")
        } finally {
            setDeleting(false)
        }
    }

    return (
        <article className="document-card">
            <Link
                className="document-card__cover"
                to={`/document/${document.id}`}
                onClick={closeSidebar}
            >
            {document.thumbnail_path ? (
                <img
                    src={`http://localhost:8000/documents/${document.id}/thumbnail`}
                    alt={`${document.name} cover`}
                    className="document-card__image"
                />
            ) : (
                <div className="document-card__placeholder">
                    <FaFilePdf />
                    <span>PDF DOCUMENT</span>
                </div>
            )}
            </Link>

            <div className="document-card__content">
                <Link
                    className="document-card__title"
                    to={`/document/${document.id}`}
                    onClick={closeSidebar}
                    title={document.name}
                >
                    {document.name}
                </Link>

                <div className="document-card__footer">
                    <span>
                        {document.page_count ?? document.page ?? 0} pages
                    </span>

                    <button
                        className="document-card__delete"
                        type="button"
                        aria-label={`Delete ${document.name}`}
                        title="Delete document"
                        disabled={deleting}
                        onClick={handleDelete}
                    >
                        <FaTrash />
                    </button>
                </div>
            </div>
        </article>
    )
}
