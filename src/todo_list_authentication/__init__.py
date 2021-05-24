from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from sqlalchemy import create_engine
from src.todo_list_authentication.models import Base, db

# db = SQLAlchemy()
# DB_NAME = "database.db"
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SuperSecretKey'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    DATABASE_URI = os.environ['DATABASE_URI']
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    # create_database(app)
    engine = create_engine(DATABASE_URI, pool_pre_ping=True)
    db_connection = engine.connect()

    try:
        create_database(engine)
    except BaseException:  # sqlalchemy.exc.IntegrityError?
        pass

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')

def create_database(engine):
    Base.__note__.drop_all(engine)
    Base.__note__.create_all(engine)

    Base.__user__.drop_all(engine)
    Base.__user__.create_all(engine)
    print('Created Database!')

