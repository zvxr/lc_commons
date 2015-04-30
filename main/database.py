
import config
import sqlite3

"""Inclues database connection class, and methods for interacting with database.
"""

def add_loans_funded_as_of_date(loans, db_conn):
    sql = """
        INSERT INTO loansFundedAsOfDate VALUES(?,?,?)
    """
    params = map(lambda loan: loan.get_funded_tuple(), loans)
    db_conn.executemany(sql, params)


def add_raw_loan_dates(date_string, db_conn):
    sql = """ INSERT OR IGNORE INTO rawLoanDates VALUES(?)"""
    params = (date_string,)
    db_conn.execute(sql, params)


def add_raw_loans(loans, db_conn):
    sql = """
        INSERT OR IGNORE INTO rawLoans VALUES(
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?
        )
    """
    params = map(lambda loan: loan.get_raw_loans_tuple(), loans)
    db_conn.executemany(sql, params)


def has_been_recorded(date_string, db_conn):
    """Return True if the epoch passed has been recorded already."""
    sql = """
        SELECT COUNT(*)
          FROM rawLoanDates
         WHERE asOfDate = (?)
    """
    params = (date_string,)
    return (db_conn.execute(sql, params, results='fetchone')[0] > 0)


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
            self._database = sqlite3.connect(config.DATABASE)
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
            return cursor.fetchone()
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
