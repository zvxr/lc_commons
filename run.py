"""Script for running Lending Club Commons project by commandline.
"""

import argparse
import config
import logging
import main.lc_commons
import main.log


def positive_int(param):
    """Validates and returns non-negative integer."""
    int_param = int(param)
    if int_param < 0:
        raise argparse.ArgumentTypeError(
            "%s must be a positive integer." % int_param
        )
    return int_param


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--database",
        "-d",
        default=config.DATABASE,
        help="Path to the database to write to."
    )

    parser.add_argument(
        "--delay",
        "-s",
        default=config.POLLING_INTERVAL,
        help="The minimum amount of time before API requests.",
        type=positive_int
    )

    parser.add_argument(
        "--log",
        "-l",
        const=config.LOG_PATH,
        default=False,
        help="Controls logging-- when specified writes to path provided.",
        nargs='?'
    )

    parser.add_argument(
        "--number-requests",
        "-n",
        default=0,
        dest="number_requests",
        help="The number of requests to make. 0 will run indefinitely.",
        nargs="?",
        type=positive_int
    )

    parser.add_argument(
        "--token",
        "-t",
        default=config.API_TOKEN,
        help="The Lending Club API token when making requests.",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="Activates stream log. First flag will set to INFO, next to DEBUG."
    )

    args = parser.parse_args()

    # Set-up logging based on verbosity.
    if args.verbose > 1:
        main.log.setup_logging(
            stream=True,
            logfile=args.log,
            stream_level=logging.DEBUG
        )
    elif args.verbose == 1:
        main.log.setup_logging(
            stream=True,
            logfile=args.log,
            stream_level=logging.INFO
        )
    else:
        main.log.setup_logging(stream=False, logfile=args.log)

    request_count = 0

    while not args.number_requests or request_count < args.number_requests:
        main.lc_commons.execute_with_delay(delay=args.delay, token=args.token)
        request_count += 1
