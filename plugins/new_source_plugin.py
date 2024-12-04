# plugins/new_source_plugin.py
import requests
from datetime import datetime
from plugins.base_plugin import BasePlugin

class NewSourcePlugin(BasePlugin):
    def __init__(self):
        self.api_endpoint = 'https://api.newsource.com/articles'  # Example API endpoint
        self.api_key = 'YOUR_API_KEY'  # Replace with your API key
        self.source = 'NewSource'

    def fetch_articles(self):
        response = requests.get(self.api_endpoint, params={'apiKey': self.api_key})
        data = response.json()
        articles = []
        for item in data.get('articles', []):
            try:
                published_at = datetime.strptime(item['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except (ValueError, KeyError):
                published_at = datetime.utcnow()
            article = {
                'title': item['title'],
                'description': item.get('description', ''),
                'url': item['url'],
                'source': self.source,
                'publishedAt': published_at
            }
            articles.append(article)
        return articles