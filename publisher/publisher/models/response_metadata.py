from datetime import datetime

from pydantic import BaseModel


class ResponseMetadata(BaseModel):
    pages: int = 1  # TODO:  Pagination to be implemented
    page: int = 1  # TODO:  Pagination to be implemented
    timestamp: datetime = datetime.now()
