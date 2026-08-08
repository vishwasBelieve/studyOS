from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile
from uuid import UUID,uuid4

from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.db.database import get_db

router = APIRouter(prefix="/documents",tags=["Documents"])

@router.get("/{document_id}")
def get_document(document_id: UUID, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "name": document.name,
        "owner_id": document.owner_id,
        "owner": document.owner.username
    }

@router.post("/",response_model=DocumentResponse)
def upload_document(file:UploadFile,db:Session = Depends(get_db)):
    stored_name = f"{uuid4()}.pdf"
    file_path = f"uploads/{stored_name}"
    with open(file_path,"wb") as buffer:
        buffer.write(file.file.read())
    document = Document(
        owner_id  = 1,
        name = file.filename,
        mime_type = file.content_type,
        size = file.size,
        page_count = 0,
        stored_name = stored_name,
        file_path = file_path
        
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document