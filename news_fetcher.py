"""Fetch today's news headlines from public RSS feeds."""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone


# Public RSS feed sources
RSS_FEEDS = {
    "BBC News": "https://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
}

DEFAULT_TIMEOUT = 10  # seconds


def fetch_rss(url, timeout=DEFAULT_TIMEOUT):
    """Fetch and parse an RSS feed from the given URL.

    Args:
        url: The RSS feed URL.
        timeout: Request timeout in seconds.

    Returns:
        A list of dicts with keys 'title', 'link', and 'published'.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NewsFetcher/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read()

    return parse_rss_xml(data)


def parse_rss_xml(xml_bytes):
    """Parse RSS XML bytes into a list of article dicts.

    Args:
        xml_bytes: Raw XML content as bytes.

    Returns:
        A list of dicts with keys 'title', 'link', and 'published'.
    """
    root = ET.fromstring(xml_bytes)
    items = root.findall(".//item")

    articles = []
    for item in items:
        title_el = item.find("title")
        link_el = item.find("link")
        pub_date_el = item.find("pubDate")

        articles.append({
            "title": title_el.text.strip() if title_el is not None and title_el.text else "",
            "link": link_el.text.strip() if link_el is not None and link_el.text else "",
            "published": pub_date_el.text.strip() if pub_date_el is not None and pub_date_el.text else "",
        })

    return articles


def fetch_news(sources=None, max_items=5):
    """Fetch top news headlines from multiple RSS sources.

    Args:
        sources: A dict mapping source names to RSS URLs.
                 Defaults to RSS_FEEDS.
        max_items: Maximum number of headlines per source.

    Returns:
        A dict mapping source names to lists of article dicts.
    """
    if sources is None:
        sources = RSS_FEEDS

    all_news = {}
    for name, url in sources.items():
        try:
            articles = fetch_rss(url)
            all_news[name] = articles[:max_items]
        except Exception as exc:
            all_news[name] = [{"title": f"Error fetching feed: {exc}", "link": "", "published": ""}]

    return all_news


def display_news(news):
    """Print news headlines to the console.

    Args:
        news: A dict mapping source names to lists of article dicts.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"\n{'='*60}")
    print(f"  Today's News Headlines — {today}")
    print(f"{'='*60}\n")

    for source, articles in news.items():
        print(f"📰 {source}")
        print(f"{'-'*40}")
        for i, article in enumerate(articles, 1):
            print(f"  {i}. {article['title']}")
            if article["link"]:
                print(f"     🔗 {article['link']}")
            if article["published"]:
                print(f"     📅 {article['published']}")
        print()


if __name__ == "__main__":
    print("Fetching today's news...")
    news = fetch_news()
    display_news(news)
