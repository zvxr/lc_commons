"""Includes logging management methods. `setup_logging` should be called when
beginning execution. The `get_logger` method should always be used for fetching
log instances.
"""

import logging
import logging.handlers
import os
import socket
import sys


_ch = None
_fh = None
host = socket.gethostname()


def _make_path(logfile):
    """Generates the string path `logfile` if it does not already exist.
    This will create directories-- make sure executing user has permissions.
    """
    filepath = os.path.dirname(logfile)
    if filepath and not os.path.exists(filepath):
        os.makedirs(filepath)


def get_logger(name):
    """Return a log instance.
    Stream/File handlers are added based on `setup_logging`.
    name parameter should be passed as `__name__`.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        if _ch:
            logger.addHandler(_ch)

        if _fh:
            logger.addHandler(_fh)

    return logger


def setup_logging(
    stream=True, logfile=None, stream_level=logging.INFO, file_level=logging.ERROR
):
    """Set-up format and verbosity.
    `stream` when True will turn on stream handler.
    `logfile` when passed (string path to log), file handler is activated.
    """
    formatter = logging.Formatter(
        "[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s".format(host)
    )

    if stream:
        global _ch
        _ch = logging.StreamHandler()
        _ch.setLevel(stream_level)
        _ch.setFormatter(formatter)
        logging.getLogger("").addHandler(_ch)

    if logfile:
        _make_path(logfile)

        global _fh
        _fh = logging.FileHandler(logfile)
        _fh.setLevel(file_level)
        _fh.setFormatter(formatter)
        logging.getLogger("").addHandler(_fh)
