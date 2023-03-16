from typing import Any, Union

from pydantic import BaseModel

from publisher.models.tracking_events.envelope import (
    Envelope,
)


class FunctionCallData(BaseModel):
    function_name: str
    parameters: Union[list[Any], None]
    returns: Union[list[Any], None]


class FunctionCall(Envelope):
    event_type: str = "functionCall"
    data: FunctionCallData
