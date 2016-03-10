
import psycopg2
import lc_commons.config as lc_config

from psycopg2.extras import RealDictCursor


def get_connection(dbname=None, dbhost=None, dbport=None, dbuser=None, dbpass=None, dict_cursor=False):
    """
    Return a psycopg2 Connection instance with specified dsn parts.
    When `dict_cursor` is True (default), will return a connection that spawns dict cursors
    as a default.

    As workers are confined to a single task, the preferred connection and cursor management
    pattern is to make use of the `with` statement. This enables a single connection to be
    established for the work required within a task (connection should never be left idle and
    should always be closed before task completes). The `with` statement can then be used to
    spawn and manage individual cursors with transaction state. More information here:

    https://pythonhosted.org/psycopg2/usage.html#with-statement

    It is also prefered that Postgres interaction is wrapped in try/except block, where
    exceptions are handled by tasks.handle_exception method. This will help manage retries
    on connection failures.
    """
    dsn = "dbname={0}".format(dbname)
    if dbhost is not None:
        dsn += " host=%s" % dbhost
    if dbport is not None:
        dsn += " port=%s" % dbport
    if dbuser is not None:
        dsn += " user=%s" % dbuser
    if dbpass is not None:
        dsn += " password=%s" % dbpass

    if dict_cursor:
        return psycopg2.connect(dsn, cursor_factory=RealDictCursor)
    else:
        return psycopg2.connect(dsn)


def get_events_connection(dict_cursor=False):
    """Return a psycopg2 Connection instance to `events` Database."""
    return get_connection(
        dbname=lc_config.POSTGRES_EVENTS_DB,
        dbhost=lc_config.POSTGRES_HOST,
        dbport=lc_config.POSTGRES_PORT,
        dbuser=lc_config.POSTGRES_USER,
        dbpass=lc_config.POSTGRES_PASSWORD,
        dict_cursor=dict_cursor
    )
