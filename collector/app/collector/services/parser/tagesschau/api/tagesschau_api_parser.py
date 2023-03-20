import logging
from datetime import datetime
from typing import Generator, Iterable, Union

from collector.models.news import News
from collector.services.parser.base.base_parser import BaseParser
from collector.services.parser.topic_mapping import TopicMapping


class TagesschauApiParser(BaseParser):
    def __init__(self):
        pass

    source: str = "tagesschau"

    def parse_news(self, news_raw: dict) -> News:
        """Parse dict of individual news article."""

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

        logging.debug("TagesschauApiParser.parse_news()")
        try:
            logging.debug(
                f"Parse news from:  {self.source},  url:  {news_raw['detailsweb']}"
            )
            news = News(
                source=self.source,
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
                source=self.source,
                title="error",
                url=str(error),  # TODO:  Use blacklist instead?
            )

        return news

    def parse_news_many(self, many_news_raw: dict) -> Iterable[News]:
        logging.debug("TagesschauApiParser.parse_news_many()")
        return map(self.parse_news, many_news_raw["news"])

    def get_tags_many(self, many_news: Iterable[News]) -> list[str]:
        all_tags = (news.tags for news in many_news if news.tags is not None)
        all_tags_flattened = (tag for sublist in all_tags for tag in sublist)

        unique_tags = sorted(list(set(all_tags_flattened)))

        return unique_tags

    def parse_keywords_many(self, many_news: Iterable[News]) -> Iterable[str]:
        return self.get_tags_many(self.parse_news_many(many_news))
