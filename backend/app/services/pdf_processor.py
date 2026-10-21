from pathlib import Path
from uuid import UUID
import logging
import pymupdf
from app.tryingFile.pdf_processing import text_extractor
from sqlalchemy.orm import Session
from app.models.document_text import DocumentText
from app.tryingFile.pdf_processing import extract_page_chunks
from app.models.document import Document  

THUMBNAIL_DIR = Path(
    "/mnt/hdd/Projects/StudyOS/backend/thumbnails"
)


logger = logging.getLogger(__name__)

def is_searchable(text: str) -> bool:
    cleaned_text = text.strip()
    return len(cleaned_text) >= 30 and len(cleaned_text.split()) >= 10

def thumbnail_extractor(
    file_path: str,
    document_id: UUID,
    database: Session,) -> str | None:
    thumbnail_file = None

    try:
        THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

        thumbnail_file = THUMBNAIL_DIR / f"{document_id}.png"

        with pymupdf.open(file_path) as doc:
            if doc.page_count == 0:
                return None

            pixmap = doc[0].get_pixmap(
                matrix=pymupdf.Matrix(0.6, 0.6),
                alpha=False,
            )
            pixmap.save(str(thumbnail_file))

        document = database.get(Document, document_id)

        if document is None:
            thumbnail_file.unlink(missing_ok=True)
            return None

        document.thumbnail_path = str(thumbnail_file)
        database.flush()

        return str(thumbnail_file)

    except Exception:
        logger.exception(
            "Thumbnail generation failed for document %s",
            document_id,
        )

        if thumbnail_file is not None:
            thumbnail_file.unlink(missing_ok=True)

        return None
      
      
def pdf_extractor(file_path:str,document_id,database:Session):
        
        doc = pymupdf.open(file_path)
        book = []

        for page_number, page in enumerate(doc, start=1):
                blocks = page.get_text("blocks")
                blocks.sort(key=lambda block : block[1])
                book.append(blocks) 


        bookPages = text_extractor(book)
        for  pageNumber,block in enumerate(bookPages,start=1):
                for textNum,text in enumerate(block):
                        page_text = DocumentText(
                                document_id =document_id,
                                page_number = pageNumber,
                                paragraph_number = textNum,
                                text = text,
                                searchable = is_searchable(text)
                        )
                        database.add(page_text)
                        
             
        database.commit()


def delete_file(file_path):
     file_path = Path(file_path)
     if file_path and file_path.exists():
          file_path.unlink()
          
def pdf_extractor_non_paraphraph(
    file_path: str,
    document_id,
    database: Session
):
    chunks = extract_page_chunks(file_path)

    for textNum, block in enumerate(chunks):
        page_text = DocumentText(
            document_id=document_id,
            page_number=block["page_number"],
            paragraph_number=textNum,
            text=block["text"],
            searchable=is_searchable(block["text"])
        )
        database.add(page_text)

    database.commit()