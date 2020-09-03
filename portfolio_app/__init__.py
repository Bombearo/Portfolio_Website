from flask import Flask
from portfolio_app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    
    from portfolio_app.main.routes import main
    from portfolio_app.users.routes import users
    from portfolio_app import models

    app.register_blueprint(main)
    app.register_blueprint(users)
    return app
