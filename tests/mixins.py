import os
import tempfile

from eggsnspam.extensions import db

from .factories import oop_orm_factories


class HealthViewTestCaseMixin(object):
    """Testcase for healthcheck endpoint"""

    base_url_path = ''

    def setUp(self):
        # Get a random temporary file to use for testing
        self.tmp_status_file = next(tempfile._get_candidate_names())
        self.app.config['HEALTHCHECK_STATUS_FILE'] = self.tmp_status_file
        super(HealthViewTestCaseMixin, self).setUp()

    def tearDown(self):
        # Clean up tmp file in case it was left behind
        super(HealthViewTestCaseMixin, self).tearDown()
        try:
            os.remove(self.tmp_status_file)
        except OSError:
            pass

    def test_healthcheck(self):
        """It gets and sets the health state of the app"""

        # initial state is up
        self.assertEqual(self.client.get(self.base_url_path + '/healthcheck').status_code, 200)

        # set state to down
        self.assertEqual(self.client.get(self.base_url_path + '/healthcheck/down').status_code, 200)

        # healthcheck state is now down
        self.assertEqual(self.client.get(self.base_url_path + '/healthcheck').status_code, 503)

        # set state to up
        self.assertEqual(self.client.get(self.base_url_path + '/healthcheck/up').status_code, 200)

        # healthcheck state is now up
        self.assertEqual(self.client.get(self.base_url_path + '/healthcheck').status_code, 200)


class OrmTestCase(object):

    def setUp(self):
        super(OrmTestCase, self).setUp()
        db.create_all()
        self.set_factory_session(db)

    def set_factory_session(self, db):
        """
        Set the session object on each factory we intend to use.

        It is required for integrating SQLAlchemy with Factories.
        """
        oop_orm_factories.BreakfastFactory._meta.sqlalchemy_session = db.session
        oop_orm_factories.IngredientFactory._meta.sqlalchemy_session = db.session
        oop_orm_factories.UserFactory._meta.sqlalchemy_session = db.session
        oop_orm_factories.UserPreferenceFactory._meta.sqlalchemy_session = db.session
        oop_orm_factories.BreakfastIngredientFactory._meta.sqlalchemy_session = db.session


class SqlFixturedTestCase(object):

    sql_fixtures = []

    def setUp(self):
        super(SqlFixturedTestCase, self).setUp()
        conn = db.session.connection()
        for sql_fixture in self.sql_fixtures:
            with open(sql_fixture) as fixture_file:
                # a little blunt, but it works
                for statement in fixture_file.read().split(";"):
                    conn.execute(statement)


class BaseDaoFixturedTestCase(SqlFixturedTestCase):

    sql_fixtures = [
        'tests/fixtures/base_dao.sql'
    ]


class PhrasebookFixturedTestCase(SqlFixturedTestCase):

    sql_fixtures = [
        'eggsnspam/table_defs/eggsnspam.sqlite3.sql',
        'tests/fixtures/eggsnspam.sql',
    ]
