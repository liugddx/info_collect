# app.py
from flask import Flask, render_template, request
from models import db, Article
from sqlalchemy import desc
from plugins.plugin_manager import PluginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
db.init_app(app)

# Initialize Plugin Manager
plugin_manager = PluginManager()

@app.route('/')
def home():
    # Get the latest 10 articles
    hot_articles = Article.query.order_by(desc(Article.published_at)).limit(10).all()
    return render_template('home.html', articles=hot_articles)

@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    if keyword:
        articles = Article.query.filter(
            Article.title.contains(keyword) | Article.description.contains(keyword)
        ).order_by(desc(Article.published_at)).all()
    else:
        articles = []
    return render_template('search.html', articles=articles, keyword=keyword)

@app.route('/sources')
def sources():
    sources = db.session.query(Article.source).distinct().all()
    sources = [s[0] for s in sources]
    return render_template('sources.html', sources=sources)

@app.route('/source/<source_name>')
def source_articles(source_name):
    articles = Article.query.filter_by(source=source_name).order_by(desc(Article.published_at)).all()
    return render_template('source_articles.html', articles=articles, source=source_name)

@app.route('/rebuild_plugins')
def rebuild_plugins():
    """
    Reload plugins (e.g., after adding a new plugin)
    """
    global plugin_manager
    plugin_manager = PluginManager()
    return "Plugins reloaded."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)