from pydantic import BaseModel

class Article(BaseModel):
    Date: str
    Title: str
    Summary: str|None = None
    Content: str
    Tags: str|None = None
    Image_url: str|None = None