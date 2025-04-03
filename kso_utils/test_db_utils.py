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

def test_get_schema_table_names():
    conn = db_utils.create_connection(db_path_str)
    names = db_utils.get_schema_table_names(conn)
    print(names)
    assert isinstance(names, list), f"get_schema_table_names should return a list, instead it returns a {type(names)}"
    # The tables in the db from the template connection are defined in 'kso_utils/db_starter/schema.py'
    # And an extra table 'sqlite_sequence', which is created due to that we use AUTOINCREMENT for the agg_... tables
    names_in_schema = ['sites', 'movies', 'photos', 'subjects', 'species', 'agg_annotations_clip', 'sqlite_sequence', 'agg_annotations_frame']
    assert names == names_in_schema, f"The list of table names is not as we would expect it from schema.py. We expect: {names_in_schema}, instead we get {names}"

def _get_row_count(conn: sqlite3.Connection, table):
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    row_count = cur.fetchone()[0]
    return row_count


def test_add_to_table():
    conn = db_utils.create_connection(db_path_str)
    # If create_db is successfull, the db has a table called "sites"
    table = "sites"
    start_row_count = _get_row_count(conn, table)
    # Add one row of data to this table, check if it exist.
    db_utils.add_to_table(
        conn, table, [(1, "a", 10, 10, 10, 10), (2, "b", 20, 20, 20, 20)],
    )
    after_row_count = _get_row_count(conn, table)
    assert after_row_count == (
        start_row_count + 2
    ), f"_insert_many did not succeed to insert 2 rows, the row count before and after the function are {start_row_count} and {after_row_count}"
    # Test if we get an error telling us that the amount of columns are wrong when data is specified wrongly
    with pytest.raises(sqlite3.Error, match="columns but"):
        db_utils.add_to_table(
            conn, table, [(1, "a", 10, 10, 10), (2, "b", 20, 20, 20)],
        )


def test_empty_table():
    conn = db_utils.create_connection(db_path_str)
    # If create_db is successfull, the db has a table called "sites"
    table = "sites"
    # Add one row of data to this table, check if it exist.
    db_utils.add_to_table(conn, table, [(3, "c", 10, 10, 10, 10)])
    row_count = _get_row_count(conn, table)
    assert (
        row_count != 0
    ), f"It failed to add a row of data to the table '{table}', making it impossible to test the function empty_table. Look more at the test of _insert_many"

    # Then check if the empty_table function removes all data
    db_utils.empty_table(conn, table)
    empty_row_count = _get_row_count(conn, table)
    assert empty_row_count == 0, f"empty_table did not remove all data, the row count is {empty_row_count}"

    # Check if the table is still exists
    table_names = db_utils.get_schema_table_names(conn)
    assert table in table_names, f"the table '{table}' does not exist anymore. empty_table should only empty the table, not delete it"

    # Also test if we get an error when we try to remove a table that does not exist
    with pytest.raises(sqlite3.Error, match="does not exist"):
        db_utils.empty_table(conn, "random")
