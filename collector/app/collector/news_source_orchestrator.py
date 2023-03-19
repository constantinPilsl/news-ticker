from typing import Generator, Union

from collector.data_source_gateways.news_source.base.base_news_api_gateway import (
    BaseNewsApiGateway,
)
from collector.data_source_gateways.news_source.tagesschau.api.tagesschau_api_gateway import (
    TagesschauApiGateway,
)
from collector.keyword_cache import KeywordCache
from collector.logging.logger import logger
from collector.models.news import News
from collector.services.parser.base.base_parser import BaseParser
from collector.services.parser.tagesschau.api.tagesschau_api_parser import (
    TagesschauApiParser,
)
import itertools

class NewsSourceOrchestrator:
    def __init__(self):
        self.cache = KeywordCache()
        self.gateways: dict[str, BaseNewsApiGateway] = {
            "tagesschau": TagesschauApiGateway(),
        }
        self.parsers: dict[str, BaseParser] = {
            "tagesschau": TagesschauApiParser(),
        }
        self.news_sources = list(self.gateways.keys())

    def get_news(self, news_source: str) -> Generator[News, None, None]:
        logger.info("methodCall: NewsSourceOrchestrator.get_news()")
        return self.parsers[news_source].parse_news_many(
            self.gateways[news_source].get_news()
        )

    def get_news_many(
        self, news_sources: Union[list[str], None] = None
    ) -> Generator[News, None, None]:
        logger.info("methodCall: NewsSourceOrchestrator.get_news_many()")
        news = []

        # TODO:  IT SHOULD BE SOMETHING LIKE THIS USING A GENERATOR EXPRESSION:
        # if news_sources is None:
        #     for news_source in self.news_sources:
        #         yield news_generator.append(self.get_news(news_source))
        # else:
        #     for news_source in news_sources:
        #         yield news_generator.append(self.get_news(news_source))

        # return itertools.chain(*news_generator)

        # TODO:  IT SHOULD BE SOMETHING LIKE THIS USING A GENERATOR EXPRESSION:
        if news_sources is None:
            for news_source in self.news_sources:
                news.extend(self.get_news(news_source))
        else:
            for news_source in news_sources:
                news.extend(self.get_news(news_source))

        return news


    def get_keywords(self, news_source: str) -> list[str]:
        logger.info("methodCall: NewsSourceOrchestrator.get_keywords()")
        cached_keywords = self.cache.get_keywords(news_source)

        if cached_keywords is None:
            self.cache.set_cache(
                news_source,
                self.parsers[news_source].parse_keywords_many(
                    self.gateways[news_source].get_news()
                ),
            )
            keywords = self.cache.get_keywords(news_source)
        else:
            keywords = cached_keywords

        return keywords

    def get_keywords_many(
        self, news_sources: Union[list[str], None] = None
    ) -> list[str]:
        logger.info("methodCall: NewsSourceOrchestrator.get_keywords_many()")
        keywords = []

        if news_sources is None:
            for news_source in self.news_sources:
                keywords.extend(self.get_keywords(news_source))
        else:
            for news_source in news_sources:
                keywords.extend(self.get_keywords(news_source))

        return keywords
