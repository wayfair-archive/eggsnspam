"""Configuration for running the test suite."""

from .base import BaseConfig


class TestingConfig(BaseConfig):
    """Uses an in-memory sqlite database for running tests."""

    # NOTE: Flask ignores variables unless they are in all caps
    TESTING = True

    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:Password-123@mssql/eggsnspam_test'
