from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Loading embedding model...")

    app.state.model = SentenceTransformer('BAAI/bge-small-en-v1.5',local_files_only=True)

    print("Embedding model ready")

    yield


app  = FastAPI(lifespan=lifespan)

class EmbeddingText(BaseModel):
    texts : list[str]

@app.post("/embed")
def create_embedding(request: EmbeddingText):
    if not request.texts:
        return {"embeddings": []}

    print(f"Received {len(request.texts)} text chunks", flush=True)

    embeddings = app.state.model.encode(
        request.texts,
        batch_size=32,
        show_progress_bar=False
    )

    print("Embedding completed", flush=True)

    return {"embeddings": embeddings.tolist()}