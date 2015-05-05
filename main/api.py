"""Includes methods for interacting with Lending Club API.
"""

import config
import log
import requests


_LOG_API_RESP = "API response [{0}]: {1}"


def get_listed_loans(token=None, show_all=True):
    """Fetches and returns dictionary JSON containing loan listings.
    If token is not specified, will use config value.
    Logs error and returns NoneType if response is not 200.
    """
    # Logging.
    logger = log.get_logger(__name__)

    # Prepare and make request.
    url = config.API_URL + config.API_LOANS_URI
    headers = {
        'Authorization': token or config.API_TOKEN,
        'Content-type': "application/json"
    }
    params = {'showAll': show_all}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        logger.debug(_LOG_API_RESP.format(response.status_code, response.text))
        return response.json()
    else:
        logger.error(_LOG_API_RESP.format(response.status_code, response.text))
