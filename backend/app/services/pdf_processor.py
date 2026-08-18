import pymupdf 
from app.db.database import SessionLocal
from app.models.document_text import DocumentText
db = SessionLocal()
try:
    with open("/mnt/hdd/Projects/StudyOS/backend/app/trial.txt",'w+') as file:
        with pymupdf.open("/mnt/hdd/Projects/StudyOS/backend/uploads/frank.pdf") as pdf:
            for page_number,page in enumerate(pdf):
                text = page.get_text()

                page_text = DocumentText(
                    document_id =" b9cb16b9-9bd4-4ccb-9965-bce64c343ae2",
                    page_number = page_number,
                    text = text
                )
                db.add(page_text)
                db.commit()
finally :
    db.close()

            