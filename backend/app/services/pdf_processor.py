from pathlib import Path

import pymupdf
from app.tryingFile.pdf_processing import text_extractor
from sqlalchemy.orm import Session
from app.models.document_text import DocumentText
from app.tryingFile.pdf_processing import extract_page_chunks

def is_searchable(text: str) -> bool:
    cleaned_text = text.strip()
    return len(cleaned_text) >= 30 and len(cleaned_text.split()) >= 10

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
          
def pdf_extractor_non_paraphraph(file_path: str, document_id, database: Session):

    book = extract_page_chunks(file_path)

    for page in book:
        for textNum, block in enumerate(page):
            page_text = DocumentText(
                document_id=document_id,
                page_number=block["page_number"],
                paragraph_number=textNum,
                text=block["text"],
                searchable=is_searchable(block["text"])
            )
            database.add(page_text)

    database.commit()
