import pymupdf 
from app.db.database import SessionLocal
from app.models.document_text import DocumentText
db = SessionLocal()
def text_extractor(file_path:str,document_id):
    try:
        with pymupdf.open(file_path) as pdf:
            for page_number,page in enumerate(pdf,start=1):
                text = page.get_text()

                page_text = DocumentText(
                    document_id =document_id,
                    page_number = page_number,
                    text = text
                )
                db.add(page_text)
        db.commit()
    finally :
        db.close()

            