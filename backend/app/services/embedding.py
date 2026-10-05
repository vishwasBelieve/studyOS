from sentence_transformers import SentenceTransformer
from app.db.database import SessionLocal
from uuid import UUID
from sqlalchemy import select
from app.models.document_text import DocumentText
from sqlalchemy.orm import Session 
db = SessionLocal()

model = SentenceTransformer('BAAI/bge-small-en-v1.5',local_files_only=True)

def embeddingTexts(documentId:UUID,db:Session):
    print("called")
    
    stmt = select(DocumentText).where(DocumentText.document_id == documentId,DocumentText.embedding.is_(None))
    rows = db.execute(stmt).scalars().all()
    texts = [row.text for row in rows]
    print(f"Embedding {len(texts)} texts...")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True
    ).tolist()

    print("Embedding finished")

    for row,embeddingArr in zip(rows,embeddings):
        row.embedding = embeddingArr
    print("it's done")
    
        

