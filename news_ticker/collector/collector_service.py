import logging
from pathlib import Path
from typing import Generator, Literal, Iterable

import yaml

from collector.models.news import News
from collector.services.is_keywords_in_news import is_keywords_in_news
from collector.data_source_gateways.tagesschau.api.wrapper import get_news as tagesschau_get_news


def get_news(sources: list[str], keywords: list[str]):

    def get_relevant_news(
        many_news: Iterable[News],
        keywords: list,
        filters: dict[Literal["title", "sub_title", "tags", "text"], bool] = {
            "title": True,
            "sub_title": True,
            "tags": True,
            "text": False,
        },
    ) -> Generator[News, None, None]:
        logging.debug("get_relevant_news()")
        return (
            news for news in many_news if is_keywords_in_news(news, keywords, filters)
        )

    logging.debug("get_news()")

    # TODO:  Dynamic source selection to be implemented
    """
    news_sources = yaml.safe_load(Path("resources/news_sources.yml").read_text())
    available_sources = []

    for source in sources:
        try:
            available_sources.append(news_sources["news_sources"][source])
        except KeyError:
            logging.warning(f"WARNING!  News Source not found:  {source}")

    if available_sources:
        for source in available_sources:
            news_sources["news_sources"][source]
    """

    many_news = tagesschau_get_news()
    return get_relevant_news(many_news, keywords)
