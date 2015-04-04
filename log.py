import logging
import logging.handlers
import os
import socket
import sys

host = socket.gethostname()

stdout_logger = logging.getLogger("stdout")
stderr_logger = logging.getLogger("stderr")

# configure python-requests log level
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)

def setup_logging(logfile, loglevel=logging.INFO):
    # make sure path exists.
    filepath = os.path.dirname
    if filepath and not os.path.exists(filepath):
        os.makedirs(filepath)

    log_format = "[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s".format(host)
    logging.basicConfig(filename=logfile, level=loglevel, format=log_format)

    sys.stderr = StdErrWrapper()
    sys.stdout = StdOutWrapper()

class StdOutWrapper(object):
    def write(self, s):
        stdout_logger.info(s.strip())

class StdErrWrapper(object):
    def write(self, s):
        stderr_logger.error(s.strip())

