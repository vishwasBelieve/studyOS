from pydantic import BaseModel

class PagesResonpse(BaseModel):
    page_number :int
    text : str


class PageResponse(BaseModel):
    page_number : int
    paragraphs : list[str]
