"""
This is an example local.py which can be used as a starting point for creating a local.py.

Note that Flask ignores attributes in this file and the Config class unless they are in all caps. This allows
for a lot of freedom to muck with the configuration / environment without polluting the config namespace.
"""

import logging

from .base import BaseConfig

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class LocalConfig(BaseConfig):
    """Local config for running the app on your local machine."""

    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:Password-123@mssql/eggsnspam'
