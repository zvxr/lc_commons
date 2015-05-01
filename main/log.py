import logging
import logging.handlers
import os
import socket
import sys


_ch = None
_fh = None
host = socket.gethostname()


def _make_path(logfile):
    filepath = os.path.dirname(logfile)
    if filepath and not os.path.exists(filepath):
        os.makedirs(filepath)


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(_ch)
        logger.addHandler(_fh)


def setup_logging(logfile=None, stream_level=logging.INFO, file_level=logging.ERROR):

    formatter = logging.Formatter(
        "[%(asctime)s] {0}/%(levelname)s/%(name)s: %(message)s".format(host)
    )

    global _ch
    _ch = logging.StreamHandler()
    _ch.setLevel(stream_level)
    _ch.setFormatter(formatter)
    logging.getLogger('').addHandler(_ch)

    if logfile:
        _make_path(logfile)

        global _fh
        _fh = logging.FileHandler(logfile)
        _fh.setLevel(file_level)
        _fh.setFormatter(formatter)
        logging.getLogger('').addHandler(_fh)
