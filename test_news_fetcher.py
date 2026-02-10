"""Tests for news_fetcher module."""

import unittest
from news_fetcher import parse_rss_xml, display_news


SAMPLE_RSS = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Sample News</title>
    <item>
      <title>First headline</title>
      <link>https://example.com/1</link>
      <pubDate>Mon, 10 Feb 2026 00:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Second headline</title>
      <link>https://example.com/2</link>
      <pubDate>Mon, 10 Feb 2026 01:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


class TestParseRssXml(unittest.TestCase):
    """Tests for the parse_rss_xml helper."""

    def test_parses_titles(self):
        articles = parse_rss_xml(SAMPLE_RSS)
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0]["title"], "First headline")
        self.assertEqual(articles[1]["title"], "Second headline")

    def test_parses_links(self):
        articles = parse_rss_xml(SAMPLE_RSS)
        self.assertEqual(articles[0]["link"], "https://example.com/1")

    def test_parses_pub_date(self):
        articles = parse_rss_xml(SAMPLE_RSS)
        self.assertEqual(articles[0]["published"], "Mon, 10 Feb 2026 00:00:00 GMT")

    def test_empty_feed(self):
        empty_rss = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>Empty</title></channel></rss>
"""
        articles = parse_rss_xml(empty_rss)
        self.assertEqual(articles, [])

    def test_missing_optional_elements(self):
        rss_no_link = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item><title>Only title</title></item>
  </channel>
</rss>
"""
        articles = parse_rss_xml(rss_no_link)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["title"], "Only title")
        self.assertEqual(articles[0]["link"], "")
        self.assertEqual(articles[0]["published"], "")


class TestDisplayNews(unittest.TestCase):
    """Tests for the display_news function (smoke test)."""

    def test_display_does_not_raise(self):
        news = {
            "Test Source": [
                {"title": "Headline", "link": "https://example.com", "published": "today"},
            ]
        }
        # Should not raise
        display_news(news)


if __name__ == "__main__":
    unittest.main()
