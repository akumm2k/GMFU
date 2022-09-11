from urllib.parse import urlparse

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
    assert parse_result.hostname.split('.')[-2]  == domain ,f'{url} aint {domain }s'