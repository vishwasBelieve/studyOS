from pathlib import Path
from app.tryingFile.try_ai import clean_text

import pymupdf 
from sqlalchemy.orm import Session
from app.models.document_text import DocumentText
def text_extractor(file_path:str,document_id,database:Session):
        book_pages = []
        clean_list = []
        with pymupdf.open(file_path) as pdf:
            for page_number,page in enumerate(pdf,start=1):
                    current_page = {'page_number':page_number,'text':page.get_text()}
                    book_pages.append(current_page)

            for i in range(0, len(book_pages), 100):
                batch = book_pages[i:i + 100]
                singleString = ""
                for pages in batch:
                    singleString += f"\nPAGE {pages['page_number']}:\n{pages['text']}\n"

                clean_list.append(clean_text(singleString))
                    

                    # text = page.get_text()
                    #     page_text = DocumentText(
                    #     document_id =document_id,
                    #     page_number = page_number,
                    #     text = text
                    # )
                # database.add(page_text)
        return clean_list


def delete_file(file_path):
     file_path = Path(file_path)
     if file_path and file_path.exists():
          file_path.unlink()
          
     