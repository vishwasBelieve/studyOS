from pathlib import Path

import pymupdf
from app.tryingFile.pdf_processing import text_extractor
from sqlalchemy.orm import Session
from app.models.document_text import DocumentText
def pdf_extractor(file_path:str,document_id,database:Session):
        
        doc = pymupdf.open(file_path)
        book = []

        for page_number, page in enumerate(doc, start=1):
                blocks = page.get_text("blocks")
                blocks.sort(key=lambda block : block[1])
                book.append(blocks) 


        bookPages = text_extractor(book)
        for  pageNumber,block in enumerate(bookPages,start=1):
                for text in block:
                        page_text = DocumentText(
                                document_id =document_id,
                                page_number = pageNumber,
                                text = text
                        )
                        database.add(page_text)
                        
             
        database.commit()


def delete_file(file_path):
     file_path = Path(file_path)
     if file_path and file_path.exists():
          file_path.unlink()
          
     