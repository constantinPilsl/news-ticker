from typing import Union

from fastapi import FastAPI, Query

import collector.collector_service as collector_service
from collector.logging.logger import logger
from collector.models.news_response import NewsResponse

app = FastAPI()


@app.get("/news/")
async def get_news(
    keywords: Union[list[str], None] = Query(default=None),
    sources: Union[list[str], None] = Query(default=["tagesschau"]),
) -> NewsResponse:

    logger.debug("get_news()")
    logger.debug(f"Sources:  {sources}")
    logger.debug(f"Type Sources:  {type(sources)}")
    logger.debug(f"keywords:  {keywords}")
    logger.debug(f"Type keywords:  {type(keywords)}")
    return NewsResponse(response=list(collector_service.get_news(sources, keywords)))
