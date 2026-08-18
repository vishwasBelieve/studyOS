from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile
from fastapi.responses import FileResponse
from uuid import UUID,uuid4
import pymupdf
from app.core.oauth2 import get_current_user
from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.db.database import get_db
from app.services.pdf_processor import text_extractor

router = APIRouter(prefix="/documents",tags=["Documents"])

@router.get("/{document_id}/file")
def get_document(document_id:UUID,db:Session =Depends(get_db),user = Depends(get_current_user)):
    document = db.query(Document).filter(Document.id == document_id, Document.owner_id == user.id).first()


    if not document:
        raise HTTPException(status_code=404,detail="Document not found")
    
    return FileResponse(document.file_path,media_type=document.mime_type,filename=document.name)


@router.get("/{document_id}",response_model=DocumentResponse)
def get_document_metadata(document_id: UUID, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document

@router.post("/",response_model=DocumentResponse)
def upload_document(file:UploadFile,db:Session = Depends(get_db),user = Depends(get_current_user)):
    print("this is even running")
    stored_name = f"{uuid4()}.pdf"
    file_path = f"uploads/{stored_name}"
    with open(file_path,"wb") as buffer:
        buffer.write(file.file.read())
    with pymupdf.open(file_path) as pdf:
        page_count = len(pdf)
 
    document = Document(
        owner_id  = user.id,
        name = file.filename,
        mime_type = file.content_type,
        size = file.size,
        page_count = page_count,
        stored_name = stored_name,
        file_path = file_path
        
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    text_extractor(file_path,document.id)
    return document