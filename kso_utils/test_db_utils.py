from pathlib import Path
import sqlite3
import pytest

import kso_utils.db_utils as db_utils


def test_create_db():
    db_path_str = "sample.db"
    conn = db_utils.create_db(db_path_str)
    assert Path(db_path_str).exists(), f"the db was not created: {db_path_str}"
    assert isinstance(
        conn, sqlite3.Connection
    ), f"Connection is not a sqlite3.Connection: {type(conn)}"
    # To test that the schema was inserted we should fetch information. Example:
    # https://www.tutorialspoint.com/check-if-a-table-exists-in-sqlite-using-python


@pytest.fixture
def connection():
    # db_path is from the template project, defined in "db_starter/projects_list.csv"
    db_path_str = "template_project.db"
    conn = db_utils.create_db(db_path_str)

    yield conn

    conn.close()
    Path(db_path_str).unlink()


def test_get_schema_table_names(connection):
    names = db_utils.get_schema_table_names(connection)
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


def test_add_to_table(connection):
    # If create_db is successfull, the db has a table called "sites"
    table = "sites"
    start_row_count = _get_row_count(connection, table)
    # Add one row of data to this table, check if it exist.
    db_utils.add_to_table(
        connection,
        table,
        [(1, "a", 10, 10, 10, 10), (2, "b", 20, 20, 20, 20)],
    )
    after_row_count = _get_row_count(connection, table)
    assert after_row_count == (
        start_row_count + 2
    ), f"_insert_many did not succeed to insert 2 rows, the row count before and after the function are {start_row_count} and {after_row_count}"
    # Test if we get an error telling us that the amount of columns are wrong when data is specified wrongly
    with pytest.raises(sqlite3.Error, match="columns but"):
        db_utils.add_to_table(
            connection,
            table,
            [(1, "a", 10, 10, 10), (2, "b", 20, 20, 20)],
        )


def test_empty_table(connection):
    # If create_db is successfull, the db has a table called "sites"
    table = "sites"
    # Add one row of data to this table, check if it exist.
    db_utils.add_to_table(connection, table, [(3, "c", 10, 10, 10, 10)])
    row_count = _get_row_count(connection, table)
    assert (
        row_count != 0
    ), f"It failed to add a row of data to the table '{table}', making it impossible to test the function empty_table. Look more at the test of _insert_many"

    # Then check if the empty_table function removes all data
    db_utils.empty_table(connection, table)
    empty_row_count = _get_row_count(connection, table)
    assert empty_row_count == 0, f"empty_table did not remove all data, the row count is {empty_row_count}"

    # Check if the table is still exists
    table_names = db_utils.get_schema_table_names(connection)
    assert table in table_names, f"the table '{table}' does not exist anymore. empty_table should only empty the table, not delete it"

    # Also test if we get an error when we try to remove a table that does not exist
    with pytest.raises(sqlite3.Error, match="does not exist"):
        db_utils.empty_table(connection, "random")
