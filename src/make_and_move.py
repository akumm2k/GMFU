# Std library imports
import os
from glob import glob
from typing import Tuple
from sys import platform

# Third party imports
import eyed3 as id3
from eyed3.id3.frames import ImageFrame
from pydub import AudioSegment

# local imports
from .utils.utils import IMG_DIR, log
from .grab_artwork import grab_artwork
from .grab_music import grab_music

def make_and_move(youtube_url: str) -> None:
    """make_and_move

    creates the audio file, sticks the artwork to it, and
    moves it to the local Apple music directory

    :param youtube_url: url to the music / audio we want
    """
    music_file, artwork_file = make(youtube_url)
    move(music_file_path=music_file, artwork_file=artwork_file)

def make(youtube_url: str) -> Tuple[str, str]:
    """make

    makes the audio file:
        grabs the music from youtube
        grabs the artwork from the interwebs
    returns the paths to them

    :param youtube_url: url to the music / audio we want
    :return: paths to the downloaded audio and artwork
    """
    music_file, music_title = grab_music(youtube_url)
    artwork_file = grab_artwork(music_title)

    music = AudioSegment.from_file(f'./{music_file}')
    music.export(f'./{music_file}', format='mp3', bitrate='320k')

    audiofile = id3.load(f'./{music_file}')
    if (audiofile.tag == None):
        audiofile.initTag()

    with open(artwork_file, 'rb') as f:
        audiofile.tag.images.set(
            type_=ImageFrame.FRONT_COVER,
            img_data=f.read(),
            mime_type='image/jpeg',
            description='song cover'
        )

    audiofile.tag.save()

    return music_file, artwork_file

def move(music_file_path: str, artwork_file: str) -> None:
    """move

    empties the intermediary directories to hold the downloaded
    audio and artwork by:
        deleting the artwork
        moving the audio to the local apple music directory

    the moved audio is then run in order to import it to the library
    the rest of the job is done by dear iCloud

    :param music_file_path: the intermediary path to the audio file
    :param artwork_file: the intermediary path to the artwork
    """
    log.info(f'Emptying {IMG_DIR}')
    empty_img_dir()

    music_file = os.path.basename(music_file_path)
    home = os.path.expanduser('~')
    apple_music_dir = \
        f'{home}/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/'

    if platform != 'darwin': # no apple music directory in other platforms
        apple_music_dir = './'

    apple_music_path = os.path.join(
        apple_music_dir,
        music_file
    )

    log.info(f'moving {music_file_path} to {apple_music_path}')
    os.rename(music_file_path, apple_music_path)

    apple_music_path = apple_music_path.replace(' ', r'\ ')
    os.system(f'open {apple_music_path}')

def empty_img_dir():
    for img in glob(os.path.join(IMG_DIR, '*')):
        os.remove(img)