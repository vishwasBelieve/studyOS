from pydantic import BaseModel
from uuid import UUID

class DocumentResponse(BaseModel):
    id : UUID
    owner_id:int
    name:str
    stored_name:str
    file_path : str
    mime_type :str
    size : int
    page_count : int 

    model_config = {
        "from_attributes": True
    }