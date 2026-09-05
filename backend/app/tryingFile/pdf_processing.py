import pymupdf
from app.core.config import settings

book_pages = []
with pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/frank.pdf") as book:
    for page_number,page in enumerate(book,start=1):
        current_page = {'page_number':page_number,'text':page.get_text()}
        book_pages.append(current_page)

