# Std library imports
import json
import os
from urllib.parse import urlparse
from random import randint
from datetime import datetime
import re
import logging as log

log.basicConfig(
    level=log.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%m-%d-%Y %I:%M:%S %p',
)

IMG_DIR = '.img'
MP3_DIR = '.mp3'
GENERIC_IMG = './generic.jpg'

def sugar_filename(sour_filename: str, extension: str = '') -> str:
    """sugar_filename polishes up the video filename

    :param sour_filename: video filename string
    :return: tweaked video filename
    """
    maybe_dot = ''

    if (extension != '' and extension[0] != '.'):
        maybe_dot = '.'

    valid_chars_patt, no_xtra_whitespace_patt = r'\W', r'( )+'
    almost_valid = re.sub(valid_chars_patt, ' ', sour_filename)
    valid = re.sub(no_xtra_whitespace_patt, ' ', almost_valid).strip()

    return re.sub(' ', '-', valid) + maybe_dot + extension

def assert_domain(url: str, domain : str):
    """assert_domain

    asserts that the given url has the given domain

    :param url: the url to be verified
    :param domain: the domain to verify the url with
    """
    parse_result = urlparse(url)
    assert parse_result.hostname.split('.')[-2]  == domain, \
        f'{url} aint {domain}s'

def random_filename(title: str = '', hidden: bool = False) -> str:
    """random_filename

    returns a random filename that maybe hidden.
    the returned filename is sweentened / polished for any
    whitespace and other unwanted weedy characters.
    the filename also contains the date and time of creation.

    :param title: the base title for the filename, defaults to ''
    :param hidden: hidden flag, defaults to False
    :return: a nice filename
    """
    sweet_title = sugar_filename(title)
    rand_num = randint(1_000_000, 3_000_000)
    date = datetime.now().strftime('%m-%d-%Y-%H:%M:%S')

    maybe_dot = ''
    if hidden: maybe_dot = '.'

    return f'{maybe_dot}{sweet_title}-{date}-{rand_num}'


def google_api_credentials() -> dict[str, str]:
    """google_api_config

    returns the Google Custom Search API credentials
    from google-api.json

    :return: json-morphed-dictionary
    """
    where = '.'
    here = os.path.basename(os.getcwd())
    if here == 'src':
        where = '..'
    elif here == 'utils':
        where = '../..'

    with open(f'{where}/google-api.json', 'r') as f:
        api_config = json.load(f)
        env_vars = {
            "developer_key": "GCS_DEVELOPER_KEY",
            "custom_search_cx": "GCS_CX"
        }

        missing = (api_config == {})
        for k, v in api_config.items():
            if v == '':
                if not os.environ.get(env_vars[k]):
                    log.error(f'{k} is missing. Put it in google-api.json or export {env_vars[k]}')
                    missing = True
                else:
                    api_config[k] = os.environ[env_vars[k]]
        if missing:
            return False

        return api_config