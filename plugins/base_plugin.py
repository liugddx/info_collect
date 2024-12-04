# plugins/base_plugin.py
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def fetch_articles(self):
        """
        Fetch articles from the source.
        Should return a list of dictionaries with keys:
        - title
        - description
        - url
        - source
        - publishedAt
        """
        pass