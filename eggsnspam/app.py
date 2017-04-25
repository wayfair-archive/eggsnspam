"""This is the file which initializes the Flask app and boostraps various modules and interfaces."""

import logging
import os

import wtforms_json

from flask import Flask

from .extensions import db
from .oop_orm import oop_orm
from .oop_phrasebook import oop_phrasebook
from .simple_phrasebook import simple_phrasebook
from .home import home


# For import *
__all__ = ['create_app']


DEFAULT_BLUEPRINTS = (
    oop_orm,
    oop_phrasebook,
    simple_phrasebook,
    home
)


def create_app():
    """Create a Flask app."""
    app = Flask(__name__)
    configure_app(app)
    configure_blueprints(app, DEFAULT_BLUEPRINTS)
    configure_extensions(app)
    configure_logging(app)

    return app


def configure_app(app):
    """Different ways of configurations."""
    if 'FLASK_CONFIG' in os.environ:
        app.config.from_object(os.environ['FLASK_CONFIG'])
    else:
        raise ValueError("No FLASK_CONFIG environment variable. Cannot load app configuration.")


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_extensions(app):
    """Initialize any extensions that we're using."""
    # flask-sqlalchemy
    db.init_app(app)

    # wtforms_json
    # this extends wtforms to use json request bodies
    wtforms_json.init()


def configure_logging(app):
    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    # Set default level on logger, which might be overwritten by handlers.
    app.logger.setLevel(app.config.get("LOG_LEVEL", logging.WARNING))
