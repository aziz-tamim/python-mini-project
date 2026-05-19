from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    from app.routes import main
    app.register_blueprint(main)

    # Error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)

    # Context processor
    # This runs before EVERY template render — injects sidebar_stats
    # automatically so base.html always has it without routes passing it
    @app.context_processor
    def inject_sidebar_stats():
        from app.db_utils import get_sidebar_stats
        try:
            return dict(sidebar_stats=get_sidebar_stats())
        except Exception:
            return dict(sidebar_stats=None)

    return app