from . import private_config

DATABASE_NAME = "pestilence"

MYSQL_BASE = "mysql+mysqldb://{user}:{passwd}@{host}/{dbname}?{options}"
USER = "pestilence_jbrunner"
DB_PASSWORD = private_config.DB_PASSWORD
HOST = "localhost"
OPTIONS = "charset=utf8"


class BaseConfig:
    """Base configuration."""
    ENV = 'base'
    SECRET_KEY = private_config.SECRET_KEY
    BCRYPT_LOG_ROUNDS = 13
    THREADS_PER_PAGE = 2
    SQLALCHEMY_DATABASE_URI = MYSQL_BASE \
        .format(user=USER, passwd=DB_PASSWORD, host=HOST, dbname=DATABASE_NAME, options=OPTIONS)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration."""
    ENV = 'production'
    DEBUG = False


