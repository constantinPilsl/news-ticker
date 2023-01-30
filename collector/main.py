from typing import Union

from fastapi import FastAPI, Query

import collector.collector_service as collector_service
import collector.models.tracking_events.api_call as api_call
from collector.logging.logger import logger, session_id
from collector.models.news_response import NewsResponse

app = FastAPI()


@app.get("/news/")
async def get_news(
    keywords: Union[list[str], None] = Query(default=None),
    sources: Union[list[str], None] = Query(default=["tagesschau"]),
) -> NewsResponse:

    logger.info("apiCall:  GET/news/")
    response = NewsResponse(
        response=list(collector_service.get_news(sources, keywords))
    )

    tracking_event = api_call.ApiCall(
        event_name="get_news",
        correlation_id=session_id,
        data=api_call.ApiCallData(
            request={
                "keywords": keywords,
                "sources": sources,
            },
            response=response.dict(),
        ),
    )
    logger.info(tracking_event.json(ensure_ascii=False))

    return response
