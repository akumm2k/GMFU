import logging as log
from googlesearch import search

from utils import assert_domain


log.basicConfig(
    filename='grab_artword.log', encoding='utf-8', level=log.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%m-%d-%Y %I:%M:%S %p',
)

def first_goo(search_str: str) -> str:
    """first_goo returns the first google search url 

    :param search_str: the search string
    :raises Exception: if there's no search results
    :return: url for the first google result
    """
    url = next(search(search_str, stop=1))
    try:
        return url
    except StopIteration:
        raise log.error(f'no result found for: {search_str}')
    


def grab_artwork(artist: str):
    """grab_artwork resturns an artwork of the given artist

    current implementation uses the artist's instagram's latest
    image
    TODO:
        - [ ] finish implementation
            - [ ] use a str similarity metric to sort of verify the 
            the artist's insta profile

    :param artist: artist name
    """
    insta_url = first_goo(f'{artist} instagram')
    assert_domain(insta_url, "instagram")