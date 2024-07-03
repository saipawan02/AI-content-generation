from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):
    Date: datetime
    Title: str
    Summary: str|None = None
    Content: str
    Tags: list|None = None
    Image_url: str|None = None