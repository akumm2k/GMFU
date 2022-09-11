# Std lib imports
from urllib.parse import urlparse
import os
from glob import glob

# Third party imports
from googlesearch import search
from instaloader import Instaloader, Profile
from google_images_search import GoogleImagesSearch

# local imports
from .utils.utils import (
    assert_domain, random_filename, google_api_credentials, 
    log, IMG_DIR,
)

def grab_artwork(music_title: str) -> str:
    """grab_artwork

    downloads the artwork for the given music_title
    TODO: redo the logic to use different sources
    
    :param music_title: music title string
    :return: artwork's file path
    """
    return from_google(music_title) # for now


def from_google(music_title: str) -> str:
    """from_google 

    downloads artwork from google for the song title using 
    Google Custom Search API

    :param music_title: the title of the song
    :return: artwork filename
    """
    filename = random_filename(music_title)
    gis = GoogleImagesSearch(**google_api_credentials())
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
    return max(glob(f'./{IMG_DIR}/*.jpg'), key=os.path.getctime)
    

def first_goo(search_str: str) -> str:
    """first_goo returns the first google search url 

    :param search_str: the search string
    :raises Exception: if there's no search results
    :return: url for the first google result
    """
    raise NotImplementedError
    url = next(search(search_str, stop=1))
    try:
        return url
    except StopIteration:
        # log.error(f'no result found for: {search_str}')
        pass
    

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
        # log.error(f'{artist_username} has no instagram posts')
    
    # latest_post = next(artist_profile.get_posts())

    # while True:
    #     if (loader.download_post(latest_post, target=artist_profile.username))
    
    # return artist_profile.username