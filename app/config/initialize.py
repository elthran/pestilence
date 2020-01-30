from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError as SqlalchemyOperationalError
from flask import Flask

from .extensions import flask_db as db
from . import private_config
from . import environment


def initialize(name):
    app = Flask(__name__)

    load_configs(app)
    load_extensions(app)

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

