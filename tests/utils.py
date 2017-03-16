import sqlalchemy


class AssertNumQueries(object):
    """
    Context manager for counting database queries

    Use as a context manager to count the number of execute()'s performed
    against the given sqlalchemy connection.

    Usage:
        with AssertNumQueries(conn, count=2):
            conn.execute("SELECT 1")
            conn.execute("SELECT 1")
    """

    def __init__(self, session, count):

        # Make sure we're starting with a blank slate by flushing any pending queries.
        session.flush()

        # Make sure we're expiring all of SQLAlchemy's caches, to avoid artificially low results.
        session.expire_all()

        self.conn = session.connection()
        self.observed_count = 0
        self.expected_count = count
        # Will have to rely on this since sqlalchemy 0.8 does not support
        # removing event listeners
        self.do_count = False
        sqlalchemy.event.listen(self.conn, 'after_execute', self.callback)

    def __enter__(self, *args):
        """No-op"""
        pass

    def __exit__(self, *args):
        """Check for equality of observed and expected counters"""
        if not self.observed_count == self.expected_count:
            raise AssertionError("Expected %d queries, but observed %d" % (self.expected_count, self.observed_count))

    def callback(self, conn, clauseelement, multiparams, params, result):
        """Increment the counter"""
        self.observed_count += 1
