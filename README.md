# 信息收集工具

一个基于 Python 和 Flask 构建的信息收集工具，用于自动聚合来自多个主流网站的文章。该工具支持关键词检索、查看文章来源、每日推荐最热文章，并提供友好的用户界面。通过插件化设计，您可以轻松扩展和集成更多的数据源。

## 目录

- [功能](#功能)
- [项目结构](#项目结构)
- [安装](#安装)
- [配置](#配置)
- [使用指南](#使用指南)
  - [运行数据收集器](#运行数据收集器)
  - [运行 Web 应用](#运行-web-应用)
- [添加新插件](#添加新插件)
- [依赖](#依赖)
- [许可证](#许可证)

## 功能

- **自动收集文章**：通过插件从多个主流来源抓取文章。
- **关键词检索**：根据用户输入的关键词搜索相关性文章。
- **查看文章来源**：浏览所有可用的文章来源并查看特定来源的文章。
- **每日推荐**：展示每日最热的文章推荐。
- **插件化设计**：支持通过插件轻松集成新的数据源。
- **用户界面**：基于 Bootstrap 的简洁、响应式网页界面。

## 项目结构

```
your_project/
│
├── app.py
├── collect_data.py
├── models.py
├── requirements.txt
├── plugins/
│   ├── __init__.py
│   ├── base_plugin.py
│   ├── plugin_manager.py
│   ├── rss_plugin.py
│   ├── web_scraper_plugin.py
│   └── new_source_plugin.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── search.html
│   ├── sources.html
│   └── source_articles.html
└── static/
    └── (可选静态文件，如 CSS、JS)
```

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/your_project.git
cd your_project
```

### 2. 创建虚拟环境

```bash
python3 -m venv env
```

### 3. 激活虚拟环境

- **Windows**

    ```bash
    env\Scripts\activate
    ```

- **macOS/Linux**

    ```bash
    source env/bin/activate
    ```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

### 1. 配置新插件

如果您使用 `new_source_plugin.py`（或其他需要 API 密钥的插件），请确保在插件代码中替换占位符 `'YOUR_API_KEY'` 为实际的 API 密钥。

例如，在 `plugins/new_source_plugin.py` 中：

```python
self.api_key = 'YOUR_ACTUAL_API_KEY'
```

### 2. 修改 RSS 源（可选）

默认的 RSS 插件抓取 BBC News 和 CNN 的 RSS 源。如需添加或修改，可以编辑 `plugins/rss_plugin.py` 中的 `self.rss_urls` 列表：

```python
self.rss_urls = [
    'https://feeds.bbci.co.uk/news/rss.xml',  # BBC News
    'http://rss.cnn.com/rss/edition.rss'      # CNN
]
```

## 使用指南

### 1. 运行数据收集器

数据收集器负责定时抓取文章并存储到数据库中。

```bash
python collect_data.py
```

此脚本会：

- 初始化数据库（`articles.db`）。
- 立即抓取一次所有已配置的数据源的文章。
- 每天早上 8 点自动抓取最新文章。

**注意**：为了在后台长期运行数据收集器，建议使用像 `screen`、`tmux` 或 `nohup` 这样的工具，或者配置系统服务。

### 2. 运行 Web 应用

启动 Flask Web 服务器，访问用户界面。

```bash
python app.py
```

默认情况下，应用将在 `http://127.0.0.1:5000/` 上运行。打开浏览器访问该地址即可查看和搜索文章。

## 添加新插件

通过插件系统，您可以轻松集成新的数据源。以下是添加新插件的步骤：

### 1. 创建新的插件文件

在 `plugins/` 目录下创建一个新的 Python 文件，例如 `my_new_plugin.py`。

### 2. 实现插件类

每个插件需要继承自 `BasePlugin` 并实现 `fetch_articles` 方法。

```python
# plugins/my_new_plugin.py
import requests
from datetime import datetime
from plugins.base_plugin import BasePlugin

class MyNewPlugin(BasePlugin):
    def __init__(self):
        self.api_endpoint = 'https://api.example.com/articles'  # 替换为实际API端点
        self.api_key = 'YOUR_API_KEY'  # 替换为实际API密钥
        self.source = 'MyNewSource'

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
```

### 3. 重新加载插件

要使新插件生效，可以通过访问 Web 应用中的 `/rebuild_plugins` 路由来重新加载插件：

```
http://127.0.0.1:5000/rebuild_plugins
```

或者重新运行 `collect_data.py` 脚本，插件管理器会自动加载新插件。

## 依赖

项目使用以下主要依赖：

- **Flask**：Web 框架
- **Flask_SQLAlchemy**：数据库 ORM
- **requests**：HTTP 请求
- **beautifulsoup4**：网页解析
- **schedule**：任务调度
- **feedparser**：RSS 解析

详细依赖列表见 `requirements.txt`。