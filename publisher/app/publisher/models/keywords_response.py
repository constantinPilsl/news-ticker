
from pydantic import BaseModel

from publisher.models.response_metadata import ResponseMetadata

class KeywordsResponse(BaseModel):
    # metadata: ResponseMetadata = ResponseMetadata()
    response: list[str]
