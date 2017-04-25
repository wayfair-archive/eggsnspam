#!/usr/bin/env python
from __future__ import print_function

import pymssql

SERVER = 'mssql'
USER = 'sa'
PASSWORD = 'Password-123'

DB_NAME = 'eggsnspam'
DB_NAME_TEST = 'eggsnspam_test'

TABLE_DEFS = 'eggsnspam/table_defs/eggsnspam.mssql.sql'
FIXTURE_DATA = 'tests/fixtures/eggsnspam.sql'


def db_exists(db_name, conn):
    """Check if database name exists"""
    sql = """
    SELECT * FROM sys.databases WHERE name = %s;
    """
    cursor = conn.cursor()
    cursor.execute(sql, db_name)
    return bool(cursor.fetchone)


def use_db(db_name, cursor):
    """Specify the database to use"""
    cursor.execute('USE {}'.format(db_name))


def create_db(db_name, conn):
    """Create the database"""
    # Autocommit is an undocumented requirement for create database statements
    conn.autocommit(True)
    sql = """
    IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = '{db_name}')
        CREATE DATABASE {db_name};
    """.format(db_name=db_name)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.autocommit(False)


def create_tables(db_name, conn):
    """Create the database"""
    with open(TABLE_DEFS) as f:
        cursor = conn.cursor()
        use_db(db_name, cursor)
        cursor.execute(f.read())
        conn.commit()


def load_fixture_data(db_name, conn):
    """Create the database"""
    with open(FIXTURE_DATA) as f:
        cursor = conn.cursor()
        use_db(db_name, cursor)
        cursor.execute(f.read())
        conn.commit()


def main():
    """Main method"""
    conn = pymssql.connect(SERVER, USER, PASSWORD)
    if not db_exists(DB_NAME, conn):
        create_db(DB_NAME, conn)
        create_tables(DB_NAME, conn)
        load_fixture_data(DB_NAME, conn)
    if not db_exists(DB_NAME_TEST, conn):
        create_db(DB_NAME_TEST, conn)

if __name__ == '__main__':
    main()
