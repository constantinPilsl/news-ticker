import logging

import collector.collector_service as collector_service
from collector.models.news_response import NewsResponse


def get_news(sources: list[str], keywords: list[str]) -> NewsResponse:
    logging.debug("get_news()")
    return NewsResponse(response=list(collector_service.get_news(sources, keywords)))
