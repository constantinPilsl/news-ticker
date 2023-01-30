import logging
from typing import Union

import requests

from publisher.models.tracking_events.api_call import ApiCall, ApiCallData


def publish_news(
    title: str,
    url: str,
    sub_title: str,
    _url: str,
    topic: str,
    session_id: Union[str, None] = None,
    **kwargs,
) -> None:
    logging.info("functionCall:  publish_news()")

    request_url = f"{_url}{topic}"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Title": title.encode("utf-8"),
        "Click": url.encode("utf-8"),
    }
    data = sub_title.encode("utf-8")

    response = requests.post(url=request_url, headers=headers, data=data)

    tracking_event = ApiCall(
        event_name="get_news",
        correlation_id=session_id,
        data=ApiCallData(
            request={
                "request_url": request_url,
                "headers": headers,
                "data": data,
            },
            response={"status_code": response.status_code},
        ),
    )
    logging.info(tracking_event.json(ensure_ascii=False))
