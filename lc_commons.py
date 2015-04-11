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
    else:
        print response.text
        raise

def execute():
    # Logging
    logger = logging.getLogger(__name__)

    # Get the loans and loan information.
    try:
        response_json = get_listed_loans()
    except:
        return

    asOfDate = response_json['asOfDate']
    asOfDateEpoch = _get_epoch(asOfDate)
    loans = [Loan(asOfDate, loan) for loan in response_json['loans']]

    # Get the connection.
    conn = sqlite3.connect(config.database)
    cursor = conn.cursor()

    # See if we have already recorded this information.
    sql = """
        SELECT COUNT(*)
          FROM rawLoanDates
         WHERE asOfDate = (?)
    """
    params = (asOfDateEpoch,)
    cursor.execute(sql, params)
    count = cursor.fetchone()[0]

    if count == 0:
        # Add raw loan date.
        sql = """ INSERT OR IGNORE INTO rawLoanDates VALUES(?)"""
        params = (asOfDate,)
        cursor.execute(sql, params)

        # Add all the raw loans, if necessary.
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
        cursor.executemany(sql, params)

        # Add loan funding.
        sql = """
            INSERT INTO loansFundedAsOfDate VALUES(?,?,?)
        """
        params = map(lambda loan: loan.get_funded_tuple(), loans)
        cursor.executemany(sql, params)

        conn.commit()
        logger.info("%s added %s loans." % (asOfDateEpoch, len(loans)))
    else:
        logger.info("%s already exists." % asOfDateEpoch)

    conn.close()

if __name__ == "__main__":
    log.setup_logging(config.log_path)

    while True:
        run_time = time.time()
        execute()
        remaining_time = config.polling_interval - (time.time() - run_time)

        if remaining_time > 0:
            time.sleep(remaining_time)
