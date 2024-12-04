# collect_data.py
from models import db, Article
from flask import Flask
from plugins.plugin_manager import PluginManager
import schedule
import time
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
db.init_app(app)

def fetch_articles():
    with app.app_context():
        manager = PluginManager()
        articles = manager.fetch_all_articles()
        new_articles = 0
        for item in articles:
            if not Article.query.filter_by(url=item['url']).first():
                article = Article(
                    title=item['title'],
                    description=item.get('description', ''),
                    url=item['url'],
                    source=item.get('source', 'Unknown'),
                    published_at=item.get('publishedAt', datetime.utcnow())
                )
                db.session.add(article)
                new_articles += 1
        if new_articles > 0:
            db.session.commit()
            print(f"Fetched and stored {new_articles} new articles.")
        else:
            print("No new articles to store.")

def run_scheduler():
    schedule.every().day.at("08:00").do(fetch_articles)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    fetch_articles()  # Fetch immediately
    run_scheduler()