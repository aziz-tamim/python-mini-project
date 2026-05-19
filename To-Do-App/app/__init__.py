from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from whitenoise import WhiteNoise
from config import Config
import os

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # WhiteNoise serves static files efficiently in production
    app.wsgi_app = WhiteNoise(
        app.wsgi_app,
        root=os.path.join(os.path.dirname(__file__), 'static'),
        prefix='static'
    )

    from app.routes import main
    app.register_blueprint(main)

    # Error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)

    # Context processor — injects sidebar_stats into every template
    @app.context_processor
    def inject_globals():
        from app.db_utils import get_sidebar_stats
        from datetime import date
        try:
            return dict(
                sidebar_stats=get_sidebar_stats(),
                today=date.today()
            )
        except Exception:
            return dict(sidebar_stats=None, today=date.today())
    return app