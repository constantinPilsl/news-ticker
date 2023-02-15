from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class News(BaseModel):
    source: str
    title: str
    sub_title: Union[str, None] = None
    tags: Union[list[str], None] = None
    text: Union[str, None] = None
    url: str = Field(description="Web url to html page")
    timestamp: datetime = datetime.now()
