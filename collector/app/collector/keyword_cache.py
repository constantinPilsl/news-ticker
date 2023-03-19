from datetime import datetime, timedelta
from typing import Union

from collector.logging.logger import logger


class KeywordCache:
    def __init__(self):
        self.keywords: Union[dict[str, dict[str, Union[set, datetime]]], None] = dict()
        self.timeout = timedelta(minutes=5)

    def set_cache(self, news_source: str, keywords: set):
        logger.info("KeywordCache.set_cache()")
        self.keywords[news_source] = {
            "keywords": keywords,
            "last_update": datetime.now(),
        }

    def get_keywords(self, news_source: str) -> set:
        logger.info("KeywordCache.get_keywords()")
        now = datetime.now()
        news_source_cache = self.keywords.get(news_source)
        if (
            news_source_cache is None
            or (now - self.keywords[news_source]["last_update"]) > self.timeout
        ):
            logger.info("KeywordCache.get_keywords() - cache miss")
            return None
        else:
            logger.info("KeywordCache.get_keywords() - cache hit")
            return news_source_cache["keywords"]
