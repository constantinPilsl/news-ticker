
from pydantic import BaseModel

from publisher.models.response_metadata import ResponseMetadata
from publisher.models.news import News

class NewsResponse(BaseModel):
    metadata: ResponseMetadata = ResponseMetadata()
    response: list[News]
