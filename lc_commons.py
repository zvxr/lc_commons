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


def execute():
    # Logging.
    logger = logging.getLogger(__name__)

    # Get the loans and loan information.
    response_json = get_listed_loans()

    if not response_json:
        logger.warn("Aborting. No API response.")
        return

    asOfDate = response_json['asOfDate']
    asOfDateEpoch = _get_epoch(asOfDate)
    loans = [Loan(asOfDate, loan) for loan in response_json['loans']]

    # Get the connection.
    ##database = SqliteDatabase.Instance()
    database = SqliteDatabase()

    # See if we have already recorded this information.
    sql = """
        SELECT COUNT(*)
          FROM rawLoanDates
         WHERE asOfDate = (?)
    """
    params = (asOfDateEpoch,)
    count = database.execute(sql, params, results='fetchone')[0]

    if count == 0:
        # Add raw loan date.
        sql = """ INSERT OR IGNORE INTO rawLoanDates VALUES(?)"""
        params = (asOfDate,)
        database.execute(sql, params)

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
        database.executemany(sql, params)

        # Add loan funding.
        sql = """
            INSERT INTO loansFundedAsOfDate VALUES(?,?,?)
        """
        params = map(lambda loan: loan.get_funded_tuple(), loans)
        database.executemany(sql, params)

        logger.info("%s added %s loans." % (asOfDateEpoch, len(loans)))
    else:
        logger.info("%s already exists." % asOfDateEpoch)

    database.close()


if __name__ == "__main__":
    log.setup_logging(config.log_path)

    while True:
        run_time = time.time()
        execute()
        remaining_time = config.polling_interval - (time.time() - run_time)

        if remaining_time > 0:
            time.sleep(remaining_time)
