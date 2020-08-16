from flask import Flask
from portfolio_app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    from portfolio_app.main.routes import main
    from portfolio_app.my_portfolio.routes import portfolio
    from portfolio_app import models

    app.register_blueprint(main)
    app.register_blueprint(portfolio)
    return app
