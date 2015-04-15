import config
import log
import logging
import requests
import time

from database import SqliteDatabase
from loans import Loan
from loans import _get_epoch


def get_listed_loans(version="v1", show_all=True):
    # Logging.
    logger = logging.getLogger(__name__)

    # Prepare and make request.
    url = "https://api.lendingclub.com/api/investor/%s/loans/listing" % version
    headers = {
        'Authorization': config.token,
        'Content-type': "application/json"
    }
    params = {'showAll': show_all}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(response.text)


def has_been_recorded(date_string, db_conn):
    """Return True if the epoch passed has been recorded already."""
    sql = """
        SELECT COUNT(*)
          FROM rawLoanDates
         WHERE asOfDate = (?)
    """
    params = (date_string,)
    return (db_conn.execute(sql, params, results='fetchone')[0] > 0)


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


def add_loans_funded_as_of_date(loans, db_conn):
    sql = """
        INSERT INTO loansFundedAsOfDate VALUES(?,?,?)
    """
    params = map(lambda loan: loan.get_funded_tuple(), loans)
    db_conn.executemany(sql, params)


def execute():
    # Logging.
    logger = logging.getLogger(__name__)

    # Get the raw loans and loan information.
    response_json = get_listed_loans()

    if not response_json:
        logger.warn("Aborting. No API response.")
        return

    asOfDate = response_json['asOfDate']
    loans = [Loan(asOfDate, loan) for loan in response_json['loans']]

    # Port over to database.
    with SqliteDatabase() as db_conn:

        if has_been_recorded(asOfDate, db_conn):
            # Populate tables.
            add_raw_loan_dates(asOfDate, db_conn)
            add_raw_loans(loans, db_conn)
            add_loans_funded_as_of_date(loans, db_conn)

            logger.info("%s added %s loans." % (asOfDate, len(loans)))
        else:
            logger.info("%s already exists." % asOfDate)


if __name__ == "__main__":
    log.setup_logging(config.log_path)

    while True:
        run_time = time.time()
        execute()
        remaining_time = config.polling_interval - (time.time() - run_time)

        if remaining_time > 0:
            time.sleep(remaining_time)
