import logging
from typing import Generator, Literal, Union

from collector.models.news import News


def is_keywords_in_news(
    news: News,
    keywords: list[str],
    filters: dict[Literal["title", "sub_title", "tags", "text"], bool] = {
        "title": True,
        "sub_title": True,
        "tags": True,
        "text": False,
    },
) -> bool:
    """Takes instance of News obje"""

    def unify_filter_object(
        filter_object: Union[list[str], str, None]
    ) -> Union[list[str], None]:
        """Transforms input into list of lowercase strings."""
        logging.debug("unify_filter_object()")
        logging.debug(f"Filter object:  {filter_object}")
        logging.debug(f"Type filter object:  {type(filter_object)}")

        if filter_object is None:
            unified_filter_object = None
        elif type(filter_object) == str:
            # TODO:  Implement as generator
            # https://stackoverflow.com/questions/3862010/is-there-a-generator-version-of-string-split-in-python
            unified_filter_object = filter_object.lower().split()
        elif type(filter_object) == list:
            # TODO:  Use generator instead
            # unified_filter_object = (i.lower() for i in filter_object)
            unified_filter_object = [i.lower() for i in filter_object]
        else:
            raise TypeError(filter_object)

        return unified_filter_object

    def is_keywords_in_filter_object(
        keywords: list[str],
        filter_object: Union[list[str], None],
    ) -> Union[bool, None]:
        logging.debug("is_keywords_in_filter_object()")
        logging.debug(f"Current filter object:  {filter_object}")
        # Alternative version that returns keyword matches
        # [word for word in filter_object if any(keyword in word for keyword in keywords)] or False
        if filter_object:
            return True in (
                True
                for word in filter_object
                if any(keyword in word for keyword in keywords)
            )

    logging.info("Apply filter is_keywords_in_news()")
    logging.debug("is_keywords_in_news()")

    news_dict = news.dict()
    filter_keys = [k for k, v in filters.items() if v]

    logging.debug(f"Filter keys:  {filter_keys}")
    logging.debug(f"Keywords:  {keywords}")
    logging.debug(f"News:  {news}")

    filter_objects = (unify_filter_object(news_dict[key]) for key in filter_keys)

    # TODO:  Implement as map or as filter function
    return True in (
        is_keywords_in_filter_object(keywords, filter_object)
        for filter_object in filter_objects
    )
