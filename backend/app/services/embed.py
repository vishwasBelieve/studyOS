
import httpx

EMBEDDING_SERVICE_URL = "http://127.0.0.1:8001/embed"


def create_embeddings(texts: list[str]) -> list[list[float]]:
    response = httpx.post(
        EMBEDDING_SERVICE_URL,
        json={"texts": texts},
        timeout=None
      
    )

    response.raise_for_status()

    return response.json()["embeddings"]
