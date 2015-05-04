"""Methods for pulling together sequential actions for polling API and recording
successful response into database.
"""

import api
import config
import database
import log
import time

from loans import Loan


def execute():
    logger = log.get_logger(__name__)

    # Get the raw loans and loan information.
    response_json = api.get_listed_loans()

    if not response_json:
        logger.warn("Aborting. No API response.")
        return

    asOfDate = response_json['asOfDate']
    loans = [Loan(asOfDate, loan) for loan in response_json['loans']]

    # Port over to database.
    with database.SqliteDatabase() as db_conn:

        if not database.has_been_recorded(asOfDate, db_conn):
            # Populate tables.
            database.add_raw_loan_dates(asOfDate, db_conn)
            database.add_raw_loans(loans, db_conn)
            database.add_loans_funded_as_of_date(loans, db_conn)

            logger.info("%s added %s loans." % (asOfDate, len(loans)))
        else:
            logger.info("%s already exists." % asOfDate)


def execute_with_delay(delay=None):
    if delay == None:
        delay = config.POLLING_INTERVAL

    run_time = time.time()
    execute()
    remaining_time = delay - (time.time() - run_time)

    if remaining_time > 0:
        time.sleep(remaining_time)


if __name__ == "__main__":
    """When executing as a script, will run indefinitely with default delay
    between requests and database inserts. For full functionality, execute the
    top level `run.py` instead.
    """
    log.setup_logging(config.LOG_PATH)

    while True:
        execute_with_delay()
