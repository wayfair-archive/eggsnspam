from flask.ext.testing import TestCase

from eggsnspam import create_app
from eggsnspam.extensions import db


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.client = self.app.test_client()

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        return app

    def tearDown(self):
        # Restore test database to a blank slate
        db.session.remove()
        db.drop_all()
