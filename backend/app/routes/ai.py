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
from app.core.oauth2 import get_current_user
from litellm import acompletion
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
async def chat_with_ai(query:Question,db:Session=Depends(get_db),user=Depends(get_current_user)):
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
    api_key = (user.ai_keys or {}).get("google")
    if not api_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Please configure your Gemini API key in settings")
    # response = requests.post("http://localhost:11434/api/chat",json={'model':'phi4-mini:latest',
    #                                                                  "messages":[{"role":"user", "content":prompt}],'stream':True},stream=True)
    #         
    response = await acompletion(
    model="gemini/gemini-3.8-flash",
    api_key=api_key,
    messages=[{"role": "user", "content": prompt}],
    stream=True,
)                                                                     
    # def genrator():
    #     for line in response.iter_lines():
    #         if line:
    #             data = json.loads(line.decode("utf-8"))

    #             if data.get('done'):
    #                 break
    #             yield data['message']['content']
    async def generator():
        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    return StreamingResponse(generator(),media_type="text/plain")
    
