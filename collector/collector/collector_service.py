from typing import Generator, Iterable, Literal

import collector.data_source_gateways.tagesschau.api.tagesschau as tagesschau_gateway
from collector.logging.logger import logger
from collector.models.news import News
from collector.services.is_keywords_in_news import is_keywords_in_news


def get_news(sources: list[str], keywords: list[str]):
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

        logger.debug("get_relevant_news()")
        return (
            news for news in many_news if is_keywords_in_news(news, keywords, filters)
        )

    logger.debug("get_news()")

    # TODO:  Dynamic source selection to be implemented
    """
    from pathlib import Path
    import yaml

    news_sources = yaml.safe_load(Path("resources/news_sources.yml").read_text())
    available_sources = []

    for source in sources:
        try:
            available_sources.append(news_sources["news_sources"][source])
        except KeyError:
            logger.warning(f"WARNING!  News Source not found:  {source}")

    if available_sources:
        for source in available_sources:
            news_sources["news_sources"][source]
    """

    many_news = tagesschau_gateway.get_news()
    return get_relevant_news(many_news, keywords)

def get_keywords(sources: list[str]) -> Generator[str, None, None]:
    # TODO:  Consider to add the option to pre-filter the tags by using
    # just the tags from relevant articles
    logger.debug("get_news()")

    # Get official tags from tagesschau
    many_news = tagesschau_gateway.get_news()

    all_tags = (news.tags for news in many_news if news.tags is not None)
    all_tags_flattened = (tag for sublist in all_tags for tag in sublist)

    unique_tags = sorted(list(set(all_tags_flattened)))

    return unique_tags
