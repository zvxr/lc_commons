
import config
import sqlite3


class SqliteDatabase(object):
    """Manages a sqlite database connection.
    May be used with the with statement.
    """
    def __init__(self):
        self._database = None

    def __enter__(self):
        return self  # lazy-load

    def __exit__(self, type, value, tb):
        self.close()

    @property
    def database(self):
        if not self._database:
            self._database = sqlite3.connect(config.database)
        return self._database

    def close(self):
        if self._database:
            self._database.close()
            self._database = None

    def execute(self, sql, params=None, results=None):
        """Wraps `cursor.execute(sql, params)`, where `params` is optional.
        Will generate a cursor for the duration of call. An optional `results`
        parameter may be set to "fetchone" or "fetchall" to return results as
        part of call.
        """
        cursor = self.database.cursor()
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            self.database.commit()
        except Exception as e:
            self.database.rollback()
            self.close()
            raise e

        if results == "fetchone":
            return  cursor.fetchone()
        elif results == "fetchall":
            return cursor.fetchall()

    def executemany(self, sql, params):
        """Wraps `cursor.executemany(sql, params)`.
        Will generate a cursor for the duration of call.
        """
        cursor = self.database.cursor()
        try:
            cursor.executemany(sql, params)
            self.database.commit()
        except Exception as e:
            self.database.rollback()
            self.close()
            raise e
