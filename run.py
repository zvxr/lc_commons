
import argparse
import config
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

    args = parser.parse_args()

    # Echo arguments
    print "database: %s" % args.database
    print "delay: %s" % args.delay
    print "log: %s" % args.log
    print "number_requests: %s" % args.number_requests
    print "token: %s" % args.token

    if args.log:
        main.log.setup_logging(args.log)

    request_count = 0

    while not args.number_requests or request_count < args.number_requests:
        main.lc_commons.execute_with_delay(delay=args.delay)
        request_count += 1
