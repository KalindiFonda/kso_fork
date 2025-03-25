from pathlib import Path
import sqlite3
import pytest

import kso_utils.db_utils as db_utils


# db_path is from the template project, defined in "db_starter/projects_list.csv"
db_path_str = "template_project.db"


def test_create_connection():
    conn = db_utils.create_connection(db_path_str)
    assert isinstance(
        conn, sqlite3.Connection
    ), f"create_connection should return a sqlite3.Connection object. Instead it returned a {type(conn)}"
    assert Path(
        db_path_str
    ).exists(), f"The database file at {db_path_str} does not exist, so it is not created and connected to successfully."

    # Test if the error message get's displayed for invalid paths
    with pytest.raises(sqlite3.Error, match="Failed to connect to"):
        db_utils.create_connection("?invalid.db")


def test_create_db():
    # This function closes previous connections, calls upon create_connection and _execute_sql.
    # Here we just check if the funtion runs. If the _execute_sql would fail because the schema.py file
    # has changed and it is not correct, the _execute_sql should fail and this function would fail.
    db_utils.create_db(db_path_str)

    # Test if the private function _execute_sql would fail with wrong SQL statements
    with pytest.raises(sqlite3.Error, match="Failed to execute the SQL statements"):
        conn = db_utils.create_connection(db_path_str)
        db_utils._execute_sql(conn, "random_string")
