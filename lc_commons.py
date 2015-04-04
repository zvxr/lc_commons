import config
import log
import logging
import requests
import sqlite3
import time

from loans import Loan
from loans import _get_epoch


def get_listed_loans(version="v1", show_all=True):
    url = "https://api.lendingclub.com/api/investor/%s/loans/listing" % version
    headers = {
        'Authorization': config.token,
        'Content-type': "application/json"
    }
    params = {'showAll': show_all}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()

def execute():
    # Logging
    logger = logging.getLogger(__name__)

    # Get the loans
    response_json = get_listed_loans()
    asOfDate = response_json['asOfDate']
    loans = [Loan(asOfDate, loan) for loan in response_json['loans']]
    asOfDateEpoch = _get_epoch(asOfDate)

    # Get the connection.
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()

    # See if we have already recorded this information.
    sql = """SELECT COUNT(*) FROM rawLoanDates WHERE asOfDate = (?)"""
    params = (asOfDateEpoch,)
    cursor.execute(sql, params)
    count = cursor.fetchone()[0]

    if count == 0:
        # Add the asOfDate if it doesn't exist.
        sql = """INSERT OR IGNORE INTO rawLoanDates(asOfDate) VALUES (?)"""
        params = (_get_epoch(asOfDate),)
        cursor.execute(sql, params)

        # Add all the loans.
        sql = """
        INSERT INTO rawLoans VALUES(
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?
        )
        """
        params = [loan.get_tuple() for loan in loans]
        cursor.executemany(sql, params)

        conn.commit()
        logger.info("%s added." % asOfDateEpoch)
    else:
        logger.info("%s already exists." % asOfDateEpoch)

    conn.close()

if __name__ == "__main__":
    log.setup_logging(config.log_path)

    while True:
        execute()
        time.sleep(60)

