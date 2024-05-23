from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import redis
from rq import Queue

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

r = redis.Redis(host='redis', port=6379)
queue = Queue(connection=r)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes import main, users, code
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(code)

    return app
