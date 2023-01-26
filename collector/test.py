import datetime
import unittest

import collector.services.is_keywords_in_news as is_keywords_in_news
from collector.logging.logger import logger
from collector.models.news import News


class TestIsKeywordsInNews(unittest.TestCase):
    def test__unify_filter_target__with_str_input(self):
        logger.debug("Execute test:  'test__unify_filter_target__with_str_input'")
        filter_target = "Keine Sonderzüge von Berlin nach München in den Winterferien"

        result = is_keywords_in_news.unify_filter_target(filter_target)
        expected = [
            "keine",
            "sonderzüge",
            "von",
            "berlin",
            "nach",
            "münchen",
            "in",
            "den",
            "winterferien",
        ]

        self.assertEqual(result, expected)

    def test__unify_filter_target__with_list_input(self):
        logger.debug("Execute test:  'test__unify_filter_target__with_list_input'")
        filter_target = ["Berlin", "Brandenburg"]

        result = is_keywords_in_news.unify_filter_target(filter_target)
        expected = ["berlin", "brandenburg"]

        self.assertEqual(result, expected)

    def test__is_keywords_in_filter_target__one_keyword_match(self):
        logger.debug(
            "Execute test:  'test__is_keywords_in_filter_target__one_keyword_match'"
        )
        keywords = ["berlin"]
        filter_target = [
            "keine",
            "sonderzüge",
            "von",
            "berlin",
            "nach",
            "münchen",
            "in",
            "den",
            "winterferien",
        ]

        result = is_keywords_in_news.is_keywords_in_filter_target(
            keywords,
            filter_target,
        )

        self.assertTrue(result)

    def test__is_keywords_in_filter_target__many_keyword_match(self):
        logger.debug(
            "Execute test:  'test__is_keywords_in_filter_target__many_keyword_match'"
        )
        keywords = ["berlin", "winterferien"]
        filter_target = [
            "keine",
            "sonderzüge",
            "von",
            "berlin",
            "nach",
            "münchen",
            "in",
            "den",
            "winterferien",
        ]

        result = is_keywords_in_news.is_keywords_in_filter_target(
            keywords,
            filter_target,
        )

        self.assertTrue(result)

    def test__is_keywords_in_filter_target__no_keyword_match(self):
        logger.debug(
            "Execute test:  'test__is_keywords_in_filter_target__no_keyword_match'"
        )
        keywords = ["budapest", "bonn"]
        filter_target = [
            "keine",
            "sonderzüge",
            "von",
            "berlin",
            "nach",
            "münchen",
            "in",
            "den",
            "winterferien",
        ]

        result = is_keywords_in_news.is_keywords_in_filter_target(
            keywords,
            filter_target,
        )

        self.assertFalse(result)

    def test__is_keywords_in_filter_target__filter_target_is_none(self):
        logger.debug(
            "Execute test:  'test__is_keywords_in_filter_target__filter_target_is_none'"
        )
        keywords = ["berlin", "winterferien"]
        filter_target = None

        result = is_keywords_in_news.is_keywords_in_filter_target(
            keywords,
            filter_target,
        )

        self.assertFalse(result)

    def test__is_keywords_in_news__one_keyword_match(self):
        logger.debug("Execute test:  'test__is_keywords_in_news__one_keyword_match'")
        news = News(
            source="tagesschau",
            title="Keine Sonderzüge von Berlin nach München in den Winterferien",
            sub_title="Die ICE-Züge von Berlin in Richtung München am kommenden Freitag und Samstag sind hoch ausgelastet.",
            tags=["Berlin", "Brandenburg"],
            text=None,
            url="https://www.tagesschau.de/ardimport/regional/brandenburg/rbb-story-115853.html",
            timestamp=datetime.datetime(
                2023,
                1,
                24,
                18,
                34,
                31,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
            ),
        )
        keywords = ["berlin"]

        result = is_keywords_in_news.is_keywords_in_news(
            news,
            keywords,
        )

        self.assertTrue(result)

    def test__is_keywords_in_news__many_keyword_match(self):
        logger.debug("Execute test:  'test__is_keywords_in_news__many_keyword_match'")
        news = News(
            source="tagesschau",
            title="Keine Sonderzüge von Berlin nach München in den Winterferien",
            sub_title="Die ICE-Züge von Berlin in Richtung München am kommenden Freitag und Samstag sind hoch ausgelastet.",
            tags=["Berlin", "Brandenburg"],
            text=None,
            url="https://www.tagesschau.de/ardimport/regional/brandenburg/rbb-story-115853.html",
            timestamp=datetime.datetime(
                2023,
                1,
                24,
                18,
                34,
                31,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
            ),
        )
        keywords = ["berlin", "winterferien"]

        result = is_keywords_in_news.is_keywords_in_news(
            news,
            keywords,
        )

        self.assertTrue(result)

    def test__is_keywords_in_news__no_keyword_match(self):
        logger.debug("Execute test:  'test__is_keywords_in_news__no_keyword_match'")
        news = News(
            source="tagesschau",
            title="Keine Sonderzüge von Berlin nach München in den Winterferien",
            sub_title="Die ICE-Züge von Berlin in Richtung München am kommenden Freitag und Samstag sind hoch ausgelastet.",
            tags=["Berlin", "Brandenburg"],
            text=None,
            url="https://www.tagesschau.de/ardimport/regional/brandenburg/rbb-story-115853.html",
            timestamp=datetime.datetime(
                2023,
                1,
                24,
                18,
                34,
                31,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
            ),
        )
        keywords = ["budapest", "bonn"]

        result = is_keywords_in_news.is_keywords_in_news(
            news,
            keywords,
        )

        self.assertFalse(result)

    def test__is_keywords_in_filter_target__filter_target_is_none_with_is_match(self):
        logger.debug(
            "Execute test:  'test__is_keywords_in_filter_target__filter_target_is_none_with_is_match'"
        )
        news = News(
            source="tagesschau",
            title="Keine Sonderzüge von Berlin nach München in den Winterferien",
            sub_title=None,
            tags=["Berlin", "Brandenburg"],
            text=None,
            url="https://www.tagesschau.de/ardimport/regional/brandenburg/rbb-story-115853.html",
            timestamp=datetime.datetime(
                2023,
                1,
                24,
                18,
                34,
                31,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
            ),
        )
        keywords = ["berlin", "winterferien"]

        result = is_keywords_in_news.is_keywords_in_news(
            news,
            keywords,
        )

        self.assertTrue(result)

    def test__is_keywords_in_filter_target__filter_target_is_none_with_is_not_match(
        self,
    ):
        logger.debug(
            "Execute test:  'test__is_keywords_in_filter_target__filter_target_is_none_with_is_not_match'"
        )
        news = News(
            source="tagesschau",
            title="Keine Sonderzüge von Berlin nach München in den Winterferien",
            sub_title=None,
            tags=["foo", "bar"],
            text=None,
            url="https://www.tagesschau.de/ardimport/regional/brandenburg/rbb-story-115853.html",
            timestamp=datetime.datetime(
                2023,
                1,
                24,
                18,
                34,
                31,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
            ),
        )
        keywords = ["budapest", "bonn"]

        result = is_keywords_in_news.is_keywords_in_news(
            news,
            keywords,
        )

        self.assertFalse(result)
