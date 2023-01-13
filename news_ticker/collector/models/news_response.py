
from pydantic import BaseModel

from collector.models.response_metadata import ResponseMetadata
from collector.models.news import News

class NewsResponse(BaseModel):
    metadata: ResponseMetadata = ResponseMetadata()
    response: list[News]
