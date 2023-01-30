import logging
from typing import Generator, Union

import requests

from publisher.models.news import News
from publisher.models.news_response import NewsResponse
from publisher.models.tracking_events.api_call import ApiCall, ApiCallData


def get_news(
    keywords: list[str],
    sources: list[str],
    url: str,
    endpoint: str,
    session_id: Union[str, None] = None,
) -> Generator[News, None, None]:

    joined_sources = "&".join((f"sources={source}" for source in sources))
    joined_keywords = "&".join((f"keywords={keyword}" for keyword in keywords))

    query_parameters = "&".join((joined_sources, joined_keywords))

    request_url = f"{url}{endpoint}/?{query_parameters}"
    response = requests.get(request_url)

    tracking_event = ApiCall(
        event_name="get_news",
        correlation_id=session_id,
        data=ApiCallData(
            request={
                "keywords": keywords,
                "sources": sources,
                "request_url": request_url,
            },
            response={"status_code": response.status_code},
        ),
    )
    logging.info(tracking_event.json(ensure_ascii=False))

    if response.status_code == 200:
        return (news for news in NewsResponse(**response.json()).response)
    else:
        error_message = f"Status code:  {response.status_code}"
        logging.warning(error_message)
        raise Exception(error_message)
