
import config
import main.database
import mock
import unittest


class TestSqliteDatabaseClass(unittest.TestCase):
    """Unit tests for Database class.
    """

    def setUp(self):
        pass

    @mock.patch('sqlite3.connect')
    def test_database(self, sqlite_connect_mock):
        connection_mock = mock.Mock()
        sqlite_connect_mock.return_value = connection_mock

        db = main.database.SqliteDatabase()
        self.assertEqual(db._database, None)
        db_conn = db.database
        self.assertEqual(db_conn, connection_mock)
        sqlite_connect_mock.assert_called_with(config.database)

    @mock.patch('main.database.SqliteDatabase.close')
    def test_with_statement(self, db_close_mock):
        with main.database.SqliteDatabase() as db_conn:
            self.assertFalse(db_close_mock.called)
        self.assertTrue(db_close_mock.called)

    def test_close(self):
        db = main.database.SqliteDatabase()
        db_conn_mock = mock.Mock()
        db._database = db_conn_mock
        db.close()
        self.assertTrue(db_conn_mock.close.called)
        self.assertEqual(db._database, None)

    @mock.patch('sqlite3.connect')
    def test_execute(self, sqlite_connect_mock):
        # Go through property for database.
        # Set-up cursor as a mock as well.
        connection_mock = mock.Mock()
        sqlite_connect_mock.return_value = connection_mock
        cursor_mock = mock.Mock()
        connection_mock.cursor.return_value = cursor_mock
        db = main.database.SqliteDatabase()

        # Test no params or results first.
        sql = "select 1"
        results = db.execute(sql)
        self.assertTrue(sqlite_connect_mock.called)
        self.assertTrue(connection_mock.cursor.called)
        cursor_mock.execute.assert_called_with(sql)
        self.assertTrue(connection_mock.commit.called)
        self.assertFalse(connection_mock.rollback.called)
        self.assertFalse(cursor_mock.fetchone.called)
        self.assertFalse(cursor_mock.fetchall.called)
        connection_mock.reset_mock()
        cursor_mock.reset_mock()
        self.assertEqual(results, None)

        # Test with params.
        params = {"name": "value"}
        results = db.execute(sql, params)
        self.assertTrue(sqlite_connect_mock.called)
        self.assertTrue(connection_mock.cursor.called)
        cursor_mock.execute.assert_called_with(sql, params)
        self.assertTrue(connection_mock.commit.called)
        self.assertFalse(connection_mock.rollback.called)
        self.assertFalse(cursor_mock.fetchone.called)
        self.assertFalse(cursor_mock.fetchall.called)
        connection_mock.reset_mock()
        cursor_mock.reset_mock()
        self.assertEqual(results, None)

        # Test with fetchone.
        results_mock = mock.Mock()
        cursor_mock.fetchone.return_value = results_mock
        results = db.execute(sql, params, results="fetchone")
        self.assertTrue(sqlite_connect_mock.called)
        self.assertTrue(connection_mock.cursor.called)
        cursor_mock.execute.assert_called_with(sql, params)
        self.assertTrue(connection_mock.commit.called)
        self.assertFalse(connection_mock.rollback.called)
        self.assertTrue(cursor_mock.fetchone.called)
        self.assertFalse(cursor_mock.fetchall.called)
        connection_mock.reset_mock()
        cursor_mock.reset_mock()
        self.assertEqual(results, results_mock)

        # Test with fetchall.
        results_mock = mock.Mock()
        cursor_mock.fetchall.return_value = results_mock
        results = db.execute(sql, params, results="fetchall")
        self.assertTrue(sqlite_connect_mock.called)
        self.assertTrue(connection_mock.cursor.called)
        cursor_mock.execute.assert_called_with(sql, params)
        self.assertTrue(connection_mock.commit.called)
        self.assertFalse(connection_mock.rollback.called)
        self.assertFalse(cursor_mock.fetchone.called)
        self.assertTrue(cursor_mock.fetchall.called)
        connection_mock.reset_mock()
        cursor_mock.reset_mock()
        self.assertEqual(results, results_mock)

        # Test an exception.
        cursor_mock.execute.side_effect = Exception("Meow!")
        self.assertRaises(Exception, db.execute, sql, params)
        self.assertTrue(cursor_mock.execute.called)
        self.assertTrue(connection_mock.rollback.called)


if __name__ == "__main__":
    unittest.main()
