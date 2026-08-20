import pymupdf 
from sqlalchemy.orm import Session
from app.models.document_text import DocumentText
def text_extractor(file_path:str,document_id,database:Session):
    
        with pymupdf.open(file_path) as pdf:
            for page_number,page in enumerate(pdf,start=1):
                text = page.get_text()

                page_text = DocumentText(
                    document_id =document_id,
                    page_number = page_number,
                    text = text
                )
                database.add(page_text)


            