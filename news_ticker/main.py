import logging

import collector.collector_controller as collector_controller
from collector.models.news_response import NewsResponse
from fastapi import FastAPI

logging.basicConfig(
    format="%(levelname)s:  %(asctime)s\t-\t%(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %I:%M:%S",
)


app = FastAPI()


@app.get("/news/")
async def get_news(
    keywords: str,
    sources: str,
) -> NewsResponse:

    return collector_controller.get_news(
        sources=[sources],
        keywords=[keywords],
    )
