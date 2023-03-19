from typing import Generator, Iterable, Literal

from collector.logging.logger import logger
from collector.models.news import News
from collector.services.is_keywords_in_news import is_keywords_in_news
from collector.news_source_orchestrator import NewsSourceOrchestrator


class CollectorService:
    news_source_orchestrator = NewsSourceOrchestrator()

    def get_news(self, news_sources: list[str], keywords: list[str]):
        def get_relevant_news(
            many_news: Iterable[News],
            keywords: list[str],
            filters: dict[Literal["title", "sub_title", "tags", "text"], bool] = {
                "title": True,
                "sub_title": True,
                "tags": True,
                "text": False,
            },
        ) -> Generator[News, None, None]:
            logger.info("functionCall: CollectorService.get_relevant_news()")
            return (
                news
                for news in many_news
                if is_keywords_in_news(news, keywords, filters)
            )

        logger.info("methodCall: CollectorService.get_news()")
        many_news = self.news_source_orchestrator.get_news_many(news_sources)

        return get_relevant_news(many_news, keywords)

    def get_keywords(self, news_sources: list[str]) -> Generator[str, None, None]:
        logger.info("methodCall: CollectorService.get_keywords()")
        return self.news_source_orchestrator.get_keywords_many(news_sources)
