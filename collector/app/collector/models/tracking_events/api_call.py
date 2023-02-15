from typing import Any, Union

from pydantic import BaseModel

from collector.models.tracking_events.envelope import (
    Envelope,
)


class ApiCallData(BaseModel):
    request: dict
    response: dict


class ApiCall(Envelope):
    event_type: str = "apiCall"
    data: ApiCallData
