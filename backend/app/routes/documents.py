import os

from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile
from fastapi.responses import FileResponse
from uuid import UUID,uuid4
import pymupdf
from app.core.oauth2 import get_current_user
from app.schemas.documentText import PagesResonpse,PageResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.document import Document
from app.models.document_text import DocumentText
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.db.database import get_db
from app.services.pdf_processor import pdf_extractor,delete_file,pdf_extractor_non_paraphraph
from app.services.embedding import embeddingTexts
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


router = APIRouter(prefix="/documents",tags=["Documents"])


@router.get("/documents")
def get_all_docs(db:Session=Depends(get_db),user = Depends(get_current_user)):
    print("running")
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    documents = db.scalars(select(Document).where(Document.owner_id == user.id).order_by(Document.created_at.desc())).all()

    return documents


@router.get("/{document_id}/file")
def get_document(document_id:UUID,db:Session =Depends(get_db),user = Depends(get_current_user)):
    document = db.query(Document).filter(Document.id == document_id, Document.owner_id == user.id).first()


    if not document:
        raise HTTPException(status_code=404,detail="Document not found")
    
    file_path = Path(document.file_path)

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="PDF file not found on the server"
        )
    
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
    stored_name = f"{uuid4()}.pdf"
    file_path = f"uploads/{stored_name}"
    try:
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
        db.flush()

        try:
            pdf_extractor(file_path,document.id,db)
        except ValueError:
            pdf_extractor_non_paraphraph(file_path,document.id,db)
        except Exception:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="can't process this pdf")


        embeddingTexts(document.id,db)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Upload failed:{e}")
        file_path = Path(file_path)
        if file_path and file_path.exists():
            file_path.unlink()
        raise
        

    
    return document

@router.get("/{document_id}/pages",response_model=list[PagesResonpse])
def get_pages(document_id:UUID,db:Session=Depends(get_db)):
    pages = db.query(DocumentText).filter(DocumentText.document_id == document_id).order_by(DocumentText.page_number).all()
    return pages

@router.delete("/{document_id}")
def delete_document(document_id:UUID,db:Session=Depends(get_db)):
    stmt = select(Document).where(Document.id == document_id)
    document = db.execute(stmt).scalar_one_or_none()
    if document is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="Document not found")
    try:
        db.delete(document)
        delete_file(document.file_path)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return {"reponse":"Deleted Successfully"}
    
@router.get("/{document_id}/pages/{page_number}",response_model=PageResponse)
def get_single_page(document_id:UUID,page_number :int,db:Session=Depends(get_db)):
    stmt = select(DocumentText.page_number,DocumentText.text).where(DocumentText.document_id == document_id,DocumentText.page_number == page_number)
    page = db.execute(stmt).all()
    response = {'page_number' : page_number,'paragraphs' : [para[1] for para in page]}
    if page is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Page not found")

    return response

