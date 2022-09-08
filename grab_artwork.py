from googlesearch import search
from utils import assert_domain

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
        raise Exception(f'no result found for: {search_str}')


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