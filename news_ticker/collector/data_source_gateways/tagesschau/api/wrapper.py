from typing import Iterable

from collector.data_source_gateways.tagesschau.api.client import Client
from collector.data_source_gateways.tagesschau.api.parser import (
    parse_news_all,
)
from collector.models.news import News


def get_news() -> Iterable[News]:
    """ Creates session,  executes get request to tagesschau api news endpoint,
        returns parsed news.
    """

    client = Client()
    news = client.get_news()

    return parse_news_all(news)
