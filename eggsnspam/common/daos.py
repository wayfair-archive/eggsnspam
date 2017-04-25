from ..extensions import db


class SqlBaseDao(object):

    MAX_RESULTS_SIZE = 500

    def __init__(self, conn=None):
        self._conn = conn

    @property
    def conn(self):
        if not self._conn or self._conn.closed:
            self._conn = db.session.connection()
        return self._conn

    def _row_to_dict(self, row):
        return dict(list(zip(list(row.keys()), row)))

    def execute(self, query, *args, **kwargs):
        """Execute a query on the database"""
        result = self.conn.execute(query, *args, **kwargs)
        return result

    def fetchone(self, query, *args, **kwargs):
        """Fetch one record from the database"""
        row = self.execute(query, *args, **kwargs).fetchone()
        if row:
            return self._row_to_dict(row)
        else:
            return None

    def fetchmany(self, query, *args, **kwargs):
        """Fetch up to MAX_RESULTS_SIZE rows"""
        results = []
        rows = self.execute(query, *args, **kwargs).fetchmany(size=self.MAX_RESULTS_SIZE)
        for row in rows:
            results.append(self._row_to_dict(row))
        return results

    def fetchall(self, query, *args, **kwargs):
        """Fetch all rows"""
        results = []
        rows = self.execute(query, *args, **kwargs).fetchall()
        for row in rows:
            results.append(self._row_to_dict(row))
        return results
