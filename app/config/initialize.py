from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError as SqlalchemyOperationalError
from flask import Flask

from .extensions import flask_db as db
from . import private_config
from . import environment
from . import hooks


def initialize(name, models=None):
    app = Flask(name.split('.')[0], static_url_path='/', static_folder='dist')

    load_configs(app)
    load_extensions(app)
    load_hooks(app)
    load_models(models)

    # Generate the initial database settings
    with app.app_context():
        try:  # an empty database can't be drop (first run only)
            print("Database dropped!")
            db.drop_all()
        except SqlalchemyOperationalError as ex:
            print('Ignore if first run.')
            print(ex)
        print("Database created")
        db.create_all()

        test_user = User("elthran")
        test_user.save()
        test_world = World()
        test_world.save()
        test_city = City(test_world.id, "Tokyo")
        test_city.save()

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

