from typing import Literal, Union

import collector.models.tracking_events.function_call as function_call
from collector.logging.logger import logger, session_id
from collector.models.news import News


def unify_filter_target(
    filter_target: Union[list[str], str, None]
) -> Union[list[str], None]:
    """Transforms input into list of lowercase strings."""
    logger.debug("functionCall:  unify_filter_target()")

    if filter_target is None:
        unified_filter_target = None
    elif type(filter_target) == str:
        # TODO:  Implement as generator
        # https://stackoverflow.com/questions/3862010/is-there-a-generator-version-of-string-split-in-python
        unified_filter_target = filter_target.lower().split()
    elif type(filter_target) == list:
        # TODO:  Use generator instead
        # unified_filter_target = (i.lower() for i in filter_target)
        unified_filter_target = [i.lower() for i in filter_target]
    else:
        raise TypeError(filter_target)

    tracking_event = function_call.FunctionCall(
        event_name="unify_filter_target",
        correlation_id=session_id,
        data=function_call.FunctionCallData(
            function_name="unify_filter_target",
            parameters=[{"filter_target": filter_target}],
            returns=[{"unified_filter_target": unified_filter_target}],
        ),
    )
    logger.debug(tracking_event.json())

    return unified_filter_target


def is_keywords_in_filter_target(
    keywords: list[str],
    filter_target: Union[list[str], None],
) -> Union[bool, None]:
    logger.debug("functionCall:  is_keywords_in_filter_target()")

    # Alternative version that returns keyword matches
    # [word for word in filter_target if any(keyword in word for keyword in keywords)] or False
    # TODO:  REMOVE AFTER DEBUG
    if filter_target:
        result = True in (
            True
            for word in filter_target
            if any(keyword in word for keyword in keywords)
        )
    else:
        result = None

    tracking_event = function_call.FunctionCall(
        event_name="is_keywords_in_filter_target",
        correlation_id=session_id,
        data=function_call.FunctionCallData(
            function_name="is_keywords_in_filter_target",
            parameters=[
                {
                    "keywords": keywords,
                    "filter_target": filter_target,
                }
            ],
            returns=[{"result": result}],
        ),
    )
    logger.debug(tracking_event.json())

    return result


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
    """Takes instance of News object and returns True if any of the passed
    keywords is present in one of the filter objects.

    A filter object can be for example the title.
    """
    logger.debug("functionCall:  is_keywords_in_news()")

    news_dict = news.dict()
    filter_keys = [k for k, v in filters.items() if v]

    filter_targets = (unify_filter_target(news_dict[key]) for key in filter_keys)

    # TODO:  Implement as map or as filter function
    result = True in (
        is_keywords_in_filter_target(keywords, filter_target)
        for filter_target in filter_targets
    )

    tracking_event = function_call.FunctionCall(
        event_name="is_keywords_in_news",
        correlation_id=session_id,
        data=function_call.FunctionCallData(
            function_name="is_keywords_in_news",
            parameters=[
                {
                    "news": news,
                    "keywords": keywords,
                    "filters": filters,
                }
            ],
            returns=[{"result": result}],
        ),
    )
    logger.debug(tracking_event.json())

    return result
