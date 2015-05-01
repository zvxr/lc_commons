
import config
import log
import requests

"""Includes methods for interacting with Lending Club API.
"""


def get_listed_loans(show_all=True):
    """Fetches and returns dictionary JSON containing loan listings.
    Logs error and returns NoneType if response is not 200.
    """
    # Logging.
    logger = log.requests_log

    # Prepare and make request.
    url = config.API_URL + config.API_LOANS_URI
    headers = {
        'Authorization': config.API_TOKEN,
        'Content-type': "application/json"
    }
    params = {'showAll': show_all}
    response = requests.get(url, headers=headers, params=params)
    import pdb; pdb.set_trace()
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(response.text)
