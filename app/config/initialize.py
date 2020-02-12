from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError as SqlalchemyOperationalError
from flask import Flask
from flask_login import LoginManager

from .extensions import flask_db as db
from . import private_config
from . import environment
from . import hooks
from ..models import User

login_manager = LoginManager()


def initialize(name, models=None):
    app = Flask(name.split('.')[0])

    load_configs(app)
    load_extensions(app)
    load_hooks(app)
    load_models(models)

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = u"You need to be logged in to see this page."

    # Generate the initial database settings
    with app.app_context():
        try:  # an empty database can't be drop (first run only)
            print("Database dropped!")
            # db.session.close()
            db.drop_all()
        except SqlalchemyOperationalError as ex:
            print('Ignore if first run.')
            print(ex)
        print("Database created")
        db.create_all()

        db.session.commit()

    return app


def load_configs(app):
    # Get configurations from private_config and environment
    app.config.from_object(private_config)
    config = getattr(environment, 'ProductionConfig')
    app.config.from_object(config)


def load_extensions(app):
    # Initialize the engine
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
    db.init_app(app)


def load_hooks(app):
    hooks.add_auto_commit(app, db)


def load_models(models):
    for model in models:
        globals()[model.__name__] = model


@login_manager.user_loader
def load_user(id_):
    try:
        return User.query.get(id_)
    except:
        return None

