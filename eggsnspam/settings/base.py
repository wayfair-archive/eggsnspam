"""Base configuration for the Flask app. It should not be used directly."""


class BaseConfig(object):
    """Configuration common to all environments."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # This needs to be unique for each Flask app, and is used to coordinate deployments
    HEALTHCHECK_STATUS_FILE = "/tmp/eggsnspam_down"
