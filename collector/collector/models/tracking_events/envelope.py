import datetime
import uuid

from pydantic import BaseModel

# TODO:  This package 
class Envelope(BaseModel):
    event_id: uuid.UUID = uuid.uuid4()
    correlation_id: uuid.UUID = uuid.uuid4()
    timestamp: datetime.datetime = datetime.datetime.now()
    event_name: str
    event_type: str
    data: dict
