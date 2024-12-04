# plugins/plugin_manager.py
import os
import importlib
from plugins.base_plugin import BasePlugin

class PluginManager:
    def __init__(self, plugins_folder='plugins'):
        self.plugins_folder = plugins_folder
        self.plugins = []
        self.load_plugins()

    def load_plugins(self):
        for filename in os.listdir(self.plugins_folder):
            if filename.endswith('.py') and filename not in ('base_plugin.py', 'plugin_manager.py', '__init__.py'):
                module_name = filename[:-3]
                module_path = f"{self.plugins_folder}.{module_name}"
                try:
                    module = importlib.import_module(module_path)
                    for attribute_name in dir(module):
                        attribute = getattr(module, attribute_name)
                        if isinstance(attribute, type) and issubclass(attribute, BasePlugin) and attribute is not BasePlugin:
                            plugin_instance = attribute()
                            self.plugins.append(plugin_instance)
                            print(f"Loaded plugin: {attribute_name}")
                except Exception as e:
                    print(f"Failed to load plugin {module_name}: {e}")

    def fetch_all_articles(self):
        all_articles = []
        for plugin in self.plugins:
            try:
                articles = plugin.fetch_articles()
                all_articles.extend(articles)
            except Exception as e:
                print(f"Error fetching articles from {plugin.__class__.__name__}: {e}")
        return all_articles