from sqlalchemy.sql.expression import text

from . import BaseTestCase
from eggsnspam.common.daos import SqlBaseDao
from eggsnspam.common.recommendations import dot_product
from .mixins import BaseDaoFixturedTestCase


class SqlBaseDaoTestCase(BaseDaoFixturedTestCase, BaseTestCase):

    def setUp(self):
        super(SqlBaseDaoTestCase, self).setUp()
        self.dao = SqlBaseDao()

    def test_fetchone(self):
        """It gets a single row"""
        query = text("""
        SELECT id, name FROM tblExample
        WHERE id=:id;
        """)
        # Expect one record to be returned
        result = self.dao.fetchone(query, id=1)
        self.assertDictEqual(result, {'id': 1, 'name': 'Foo'})

        # Expect None to be returned if
        result = self.dao.fetchone(query, id=-1)
        self.assertEqual(result, None)

        # Expect one record to be returned even if multiple rows
        result = self.dao.fetchone('SELECT id, name FROM tblExample ORDER BY id')
        self.assertDictEqual(result, {'id': 1, 'name': 'Foo'})

    def test_fetchall(self):
        """It gets all rows"""
        query = text("""
        SELECT id, name FROM tblExample
        ORDER BY id
        """)

        # Expect multiple records to be returned
        result = self.dao.fetchall(query)
        self.assertEqual(len(result), 3)
        self.assertDictEqual(result[0], {'id': 1, 'name': 'Foo'})
        self.assertDictEqual(result[1], {'id': 2, 'name': 'Bar'})
        self.assertDictEqual(result[2], {'id': 3, 'name': 'Baz'})

    def test_fetchmany(self):
        """It gets many rows"""
        query = text("""
        SELECT id, name FROM tblExample
        ORDER BY id
        """)

        # Expect multiple records to be returned
        result = self.dao.fetchmany(query)
        self.assertEqual(len(result), 3)
        self.assertDictEqual(result[0], {'id': 1, 'name': 'Foo'})
        self.assertDictEqual(result[1], {'id': 2, 'name': 'Bar'})
        self.assertDictEqual(result[2], {'id': 3, 'name': 'Baz'})

        # Expect rows to be limited by MAX_RESULTS_SIZE
        self.dao.MAX_RESULTS_SIZE = 2
        result = self.dao.fetchmany(query)
        self.assertEqual(len(result), 2)


class DotProductTestCase(BaseTestCase):

    def test_dot_product(self):
        """It gets the dot product of two dictionaries of values"""
        d1 = {
            'foo': 0.1,
            'bar': 0.2,
            'baz': 0.4
        }

        d2 = {
            'bar': 0.5,
            'baz': 1,
        }

        # expect dotproduct to = (foo(0) + bar(0.1) + baz(0.4))
        self.assertEqual(dot_product(d1, d2), 0.5)
