from pydantic import BaseModel
from uuid import UUID
class Question(BaseModel):
    question : str
    page_number : int
    document_id : UUID

class Answer(BaseModel):
    answr : str