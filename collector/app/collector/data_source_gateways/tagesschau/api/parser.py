import logging
from datetime import datetime
from typing import Iterable, Union

from collector.models.news import News


def parse_news(news_raw: dict) -> News:
    """Parse dict of individual news article."""

    # TODO:  Should come from somewhere else
    source = "tagesschau"

    def parse_tags(tags: list[dict]) -> list[Union[str, None]]:
        """Unpacks list of {"tag": "value"} pairs and returns list
            of unqiue tag values in lowercase.

        Example:
            Input
                [{'tag': 'Berlin'}, {'tag': 'Brandenburg'}]

            Returns
                ['Berlin', 'Brandenburg']
        """
        logging.debug("parse_tags()")
        return list(set([i["tag"].lower() for i in tags]))

    logging.debug("parse_news()")
    try:
        logging.debug(f"Parse news from:  {source},  url:  {news_raw['detailsweb']}")
        news = News(
            source=source,
            title=news_raw["title"],
            sub_title=news_raw["firstSentence"],
            tags=parse_tags(news_raw["tags"]),
            url=news_raw["detailsweb"],
            timestamp=datetime.fromisoformat(news_raw["date"]),
        )
    # TODO:  Replace with proper exception and exception handling
    except KeyError as error:
        logging.warning(f"{error}\tarticle.get('type'):  {news_raw.get('type')}")
        logging.warning(f"\tarticle.get('shareURL'):  {news_raw.get('shareURL')}")
        news = News(
            source=source,
            title="error",
            url=str(error),  # TODO:  Use blacklist instead?
        )

    return news


def parse_news_all(many_news_raw: dict) -> Iterable[News]:
    logging.debug("parse_news_all()")
    return map(parse_news, many_news_raw["news"])
