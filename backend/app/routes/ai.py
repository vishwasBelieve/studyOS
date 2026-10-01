from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile
from fastapi.responses import StreamingResponse
from app.schemas.ai import Question,Answer
import requests
import json

router = APIRouter(prefix="/ai",tags=["Documents"])

@router.post("/chat",response_class = StreamingResponse)
def chat_with_it(question:Question):
    print(question.document_id,question.page_number,question.question)
    response = requests.post("http://127.0.0.1:11434/api/chat",json={'model':'phi4-mini:latest',
                                                                     "messages":[{"role":"user",
                                                                                  "content":question.question}],'stream':True},stream=True)
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))

            if data.get('done'):
                break
            yield data['message']['content']
    
    