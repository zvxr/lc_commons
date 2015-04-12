
import config
import sqlite3

from util import Singleton


@Singleton
class SqliteDatabase(object):
    """Manages a single sqlite database connection.
    Call using `Instance`.
    """
    def __init__(self):
        self._database = None

    @property
    def database(self):
        if not self._database:
            self._database = sqlite3.connect(config.database)
        return self._database

    def execute(self, sql, params=None, results=None):
        """Wraps `cursor.execute(sql, params)`, where `params` is optional.
        Will generate a cursor for the duration of call. An optional `results`
        parameter may be set to "fetchone" or "fetchall" to return results as
        part of call.
        """
        try:
            cursor = self.database.cursor()

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
        try:
            cursor = self.database.cursor()
            cursor.executemany(sql, params)
            self.database.commit()
        except Exception as e:
            self.database.rollback()
            self.close()
            raise e

    def close(self):
        if self._database:
            self._database.close()
            self._database = None
