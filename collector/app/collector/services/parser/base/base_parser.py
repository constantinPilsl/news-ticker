from typing import Iterable, Generator

from collector.models.news import News


class BaseParser:
    source: str

    def parse_news_many() -> Iterable[News]:
        raise NotImplementedError

    def parse_keywords_many() -> Generator[str, None, None]:
        raise NotImplementedError
