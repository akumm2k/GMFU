from urllib.parse import urlparse

def assert_domain(url: str, domain : str):
    parse_result = urlparse(url)
    assert parse_result.hostname.split('.')[-2]  == domain ,f'{url} aint {domain }s'