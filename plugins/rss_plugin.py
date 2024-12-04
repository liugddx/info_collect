# plugins/rss_plugin.py
import feedparser
from datetime import datetime
from plugins.base_plugin import BasePlugin

class RSSPlugin(BasePlugin):
    def __init__(self):
        self.rss_urls = [
            'https://feeds.bbci.co.uk/news/rss.xml',  # BBC News
            'http://rss.cnn.com/rss/edition.rss'      # CNN
        ]

    def fetch_articles(self):
        articles = []
        for rss_url in self.rss_urls:
            feed = feedparser.parse(rss_url)
            source = feed.feed.get('title', 'Unknown Source')
            for entry in feed.entries:
                try:
                    published_at = datetime(*entry.published_parsed[:6])
                except AttributeError:
                    published_at = datetime.utcnow()
                article = {
                    'title': entry.title,
                    'description': entry.summary if 'summary' in entry else '',
                    'url': entry.link,
                    'source': source,
                    'publishedAt': published_at
                }
                articles.append(article)
        return articles