# Std lib imports
import logging as log
from urllib.parse import urlparse

# Third party imports
from googlesearch import search
from instaloader import Instaloader, Profile
from google_images_search import GoogleImagesSearch

# local imports
from utils import assert_domain, random_filename, google_api_config


log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%m-%d-%Y %I:%M:%S %p',
)

def from_google(music_title: str):
    """from_google 

    downloads artwork from google for the song title using 
    Google Custom Search API

    :param music_title: the title of the song
    :return: artwork filename
    """
    filename = random_filename(music_title, hidden=True)
    gis = GoogleImagesSearch(**google_api_config())
    search_params = {
        'q': music_title,
        'num': 1,
        'fileType': 'jpg',
        'imgSize': 'xxlarge',
    }
    gis.search(search_params=search_params, path_to_dir='./', custom_image_name=filename)
    return filename

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
    

def from_instagram(artist: str) -> str:
    """from_instagram resturns an artwork of the given artist

    current implementation uses the artist's instagram's latest
    image
    TODO: implement seamless downloads, managing empty 
        and fully consumed profiles

    :param artist: artist name
    :return: img filename
    """
    raise NotImplementedError

    insta_url = first_goo(f'{artist} instagram')
    assert_domain(insta_url, domain='instagram')

    artist_username = urlparse(insta_url).path.replace('/', '') # path = '/{artist}'
    loader = Instaloader(
        quiet=True,
        save_metadata=False,
        download_videos=False,
    )
    artist_profile = Profile.from_username(loader.context, artist_username)
    posts = artist_profile.get_posts()
    print(artist_username)
    if posts.count == 0:
        print('ok')
        log.error(f'{artist_username} has no instagram posts')
    
    # latest_post = next(artist_profile.get_posts())

    # while True:
    #     if (loader.download_post(latest_post, target=artist_profile.username))
    
    # return artist_profile.username