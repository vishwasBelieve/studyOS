from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile
from fastapi.responses import StreamingResponse
from app.schemas.ai import Question
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.embedding import model
from pgvector.sqlalchemy import VECTOR
from sqlalchemy import select
from app.models.document_text import DocumentText
from app.services.ai_services import promptMaker
import requests
import json

router = APIRouter(prefix="/ai",tags=["Documents"])

# @router.post("/chat",response_class = StreamingResponse)
# def chat_with_ai(query:Question):
    # response = requests.post("http://127.0.0.1:11434/api/chat",json={'model':'phi4-mini:latest',
    #                                                                  "messages":[{"role":"user",
    #                                                                               "content":query.question}],'stream':True},stream=True)
    # def genrator():
    #     for line in response.iter_lines():
    #         if line:
    #             data = json.loads(line.decode("utf-8"))

    #             if data.get('done'):
    #                 break
    #             yield data['message']['content']

    # return StreamingResponse(genrator(),media_type="text/plain")
@router.post("/chat")
def chat_with_ai(query:Question,db:Session=Depends(get_db)):
    question  = query.question
    query_embedding = model.encode(question)
    stmt = select(DocumentText.id,
        DocumentText.page_number,
        DocumentText.text,
        DocumentText.embedding.cosine_distance(query_embedding).label("distance"),).where(DocumentText.document_id == query.document_id,DocumentText.embedding.is_not(None),DocumentText.searchable.is_(True)).order_by(DocumentText.embedding.cosine_distance(query_embedding)).limit(5)
    result = db.execute(stmt).mappings().all()
    result.sort(key=lambda x:x['page_number'])
    for row in result:
        print(
            f"Page: {row['page_number']} | "
            f"Distance: {row['distance']}\n"
            f"{row['text']}\n")
    prompt = promptMaker(query.question,result)
    response = requests.post("http://localhost:11434/api/chat",json={'model':'phi4-mini:latest',
                                                                     "messages":[{"role":"user",
                                                                                  "content":prompt}],'stream':True},stream=True)
    def genrator():
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))

                if data.get('done'):
                    break
                yield data['message']['content']

    return StreamingResponse(genrator(),media_type="text/plain")
    
