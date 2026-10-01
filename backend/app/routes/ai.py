from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile
from fastapi.responses import StreamingResponse
from app.schemas.ai import Question
import requests
import json

router = APIRouter(prefix="/ai",tags=["Documents"])

@router.post("/chat",response_class = StreamingResponse)
def chat_with_it(query:Question):
    response = requests.post("http://127.0.0.1:11434/api/chat",json={'model':'phi4-mini:latest',
                                                                     "messages":[{"role":"user",
                                                                                  "content":query.question}],'stream':True},stream=True)
    def genrator():
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))

                if data.get('done'):
                    break
                yield data['message']['content']

    return StreamingResponse(genrator(),media_type="text/plain")
    