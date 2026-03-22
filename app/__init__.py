from flask import Flask
from .database import init_db

def create_app(config=None):
    app = Flask(__name__)

    # configuration
    app.config['DATABASE'] = 'sports_calendar.db'
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    if config:
        app.config.update(config)

    # DB initialization
    init_db(app)

    # Blueprint Registration
    from .routes import bp
    app.register_blueprint(bp)
    
    return app