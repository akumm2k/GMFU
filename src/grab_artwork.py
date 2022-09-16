# Std lib imports
from urllib.parse import urlparse
import os
from glob import glob
from typing import Union, Optional
import random

# Third party imports
from googlesearch import search
from instaloader import Instaloader, Profile
from google_images_search import GoogleImagesSearch

# local imports
from .utils.utils import (
    GENERIC_IMG, assert_domain, random_filename, google_api_credentials, 
    log, IMG_DIR, GENERIC_IMG, 
)

def grab_artwork(music_title: str, artist: Optional[str] = None) -> str:
    """grab_artwork

    downloads the artwork for the given music_title
    TODO: use top level arg parser to determine artist name, 
        and artwork download source
    
    :param music_title: music title string
    :return: artwork's file path
    """
    creds = google_api_credentials()
    if creds:
        return from_google(music_title, creds)
    log.info('Using instagram to fetch artwork')
    return from_instagram(artist)


def from_google(music_title: str, creds: str, 
artist: Optional[str] = None) -> str:
    """from_google 

    downloads artwork from google for the song title using 
    Google Custom Search API

    :param music_title: the title of the song
    :param creds: google custom search API credentials
    :return: artwork filename
    """
    filename = random_filename(music_title)

    gis = GoogleImagesSearch(**creds)
    search_params = {
        'q': music_title,
        'num': 1,
        'fileType': 'jpg',
        'imgSize': 'xxlarge',
    }

    # download image
    gis.search(
        search_params=search_params, path_to_dir=f'./{IMG_DIR}', 
        custom_image_name=filename
    ) 

    # for some weird reason gis doesn't rename the image sometimes
    if os.path.exists(f'./{IMG_DIR}/{filename}'):
        # if gis named image correctly
        return filename
    # else return the latest downloaded image
    imgs = glob(os.path.join(IMG_DIR, '*.jpg'))
    if imgs:
        return max(imgs, key=os.path.getctime)

    log.info('google download failed. Using generic image')
    return GENERIC_IMG
    

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
        log.info(f'no google result found for: {search_str}')
        return False
    

def from_instagram(artist: Optional[str] = None) -> str:
    """from_instagram resturns an artwork of the given artist

    we rely on google's top search result to give us the correct 
        instagram profile
    current implementation uses the artist's instagram's latest
        image
    TODO: implement seamless downloads, managing empty 
        and fully consumed profiles

    :param artist: artist name
    :return: img filename
    """
    if artist is None: artist = input('Enter artist name: ')
    insta_url = first_goo(f'{artist} instagram')
    if not insta_url: return GENERIC_IMG
    assert_domain(insta_url, domain='instagram') # for now

    artist_username = urlparse(insta_url).path.replace('/', '') # path = '/{artist}'
    loader = Instaloader(
        dirname_pattern=IMG_DIR,
        quiet=True,
        save_metadata=False,
        download_videos=False,
    )
    artist_profile = Profile.from_username(loader.context, artist_username)
    posts = artist_profile.get_posts()
    if posts.count == 0:
        log.info(f'{artist_username} has no instagram posts')
        return GENERIC_IMG

    latest_post = next(artist_profile.get_posts())

    downlaoded = loader.download_post(latest_post, target=artist_profile.username)
    if downlaoded:
        post_imgs = glob(os.path.join(IMG_DIR, '*.jpg'))
        return random.choice(post_imgs)

    log.info('instagram download failed. Using generic cover')
    return GENERIC_IMG