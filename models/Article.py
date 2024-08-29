from pydantic import BaseModel

class Article(BaseModel):
    Date: str
    Title: str
    is_published: bool = False
    Summary: str|None = None
    Content: str
    Tags: str|None = None
    Image_id: str|None = None