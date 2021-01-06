import unittest
from unittest.mock import MagicMock, call

from common import execute_multiple_statements, execute_statement

copy_queries = [
    # Claimant
    """
    CREATE TABLE IF NOT EXISTS claimant_stage LIKE claimant_old;
    INSERT INTO claimant_stage (id, data) SELECT id, data from claimant_old;
    """,

    # Contract
    """
    CREATE TABLE IF NOT EXISTS contract_stage LIKE contract_old;
    INSERT contract_stage (id, data) SELECT id, data from contract_old;
    """,

    # Statement
    """
    CREATE TABLE IF NOT EXISTS statement_stage LIKE statement_old;
    INSERT statement_stage (id, data) SELECT id, data from statement_old;
    """
]

drop_query = """
DROP TABLE IF EXISTS claimant;
DROP TABLE IF EXISTS contract;
DROP TABLE IF EXISTS statement;
"""

rename_query = """
RENAME TABLE claimant_stage TO claimant,
             contract_stage TO contract,
             statement_stage TO statement;
"""


class TestDatabase(unittest.TestCase):
    def test_copy_queries(self):
        execute_mock = MagicMock()
        execute_mock.with_rows = True

        cursor_mock = MagicMock()
        cursor_mock.description = [("id"), ("data")]
        cursor_mock.execute.return_value = [execute_mock]

        connection_mock = MagicMock()
        connection_mock.cursor.return_value = cursor_mock

        for query in copy_queries:
            execute_multiple_statements(query, connection_mock)

        expected_calls = [call(i, multi=True) for i in copy_queries]

        cursor_mock.execute.assert_has_calls(expected_calls)
        self.assertEqual(3, cursor_mock.execute.call_count)

    def test_drop_query(self):
        execute_mock = MagicMock()
        execute_mock.with_rows = True

        cursor_mock = MagicMock()
        # cursor_mock.description = [("id"), ("data")]
        cursor_mock.execute.return_value = [execute_mock]

        connection_mock = MagicMock()
        connection_mock.cursor.return_value = cursor_mock

        execute_multiple_statements(drop_query, connection_mock)

        cursor_mock.execute.assert_called_once_with(drop_query, multi=True)

    def test_rename_query(self):
        cursor_mock = MagicMock()
        connection_mock = MagicMock()
        connection_mock.cursor.return_value = cursor_mock

        execute_statement(rename_query, connection_mock)

        cursor_mock.execute.assert_called_once_with(rename_query)


if __name__ == '__main__':
    unittest.main()
