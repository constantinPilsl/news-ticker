from time import sleep

from config import Config

import publisher.data_source_gateways.collector.collector as collector_gateway
from publisher.publisher_service import publish_news

config = Config()


keywords = [
    "litauen",
]

news_response = collector_gateway.get_news(
    keywords=keywords,
    sources=["tagesschau"],
    url=config.collector["url"],
    endpoint=config.collector["endpoints"]["news"],
    session_id=config.session_id
)

for news in news_response:
    sleep(2)
    publish_news(
        _url=config.publisher["url"],
        topic=config.publisher["topics"][config.env],
        session_id=config.session_id,
        **news.dict(),
    )
