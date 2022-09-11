import json 
from urllib.parse import urlparse
from random import randint
from datetime import datetime

def sugar_filename(sour_filename: str, extension: str = '') -> str:
    """sugar_filename polishes up the video filename

    :param sour_filename: video filename string
    :return: tweaked video filename
    """
    maybe_dot = ''

    if (extension != '' and extension[0] != '.'):
        maybe_dot = '.'

    return (sour_filename.strip()
        .replace(' ', '-')
        .replace('/', '-')
    ) + maybe_dot + extension

def assert_domain(url: str, domain : str):
    parse_result = urlparse(url)
    assert parse_result.hostname.split('.')[-2]  == domain, \
        f'{url} aint {domain}s'

def random_filename(title: str = '', hidden: bool = False):
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


def google_api_config():
    with open('./google-api.json', 'r') as f:
        api_config = json.load(f)
        
        missing = False
        for k, v in api_config.items():
            if v == '':
                print(f'{k} is missing in google_api_config')
                missing = True
        assert not missing, 'Missing google api config'

        return api_config