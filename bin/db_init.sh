#!/bin/bash
cat eggsnspam/table_defs/eggsnspam.sqlite3.sql | sqlite3 eggsnspam.db
cat tests/fixtures/eggsnspam.sql | sqlite3 eggsnspam.db
