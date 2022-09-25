# Std lib imports
import argparse
import os
from sys import platform

# local imports
from src.make_and_move import make_and_move
from src.grab_music import grab_music, validate_url
from src.utils.utils import sugar_filename

# if __name__ == '__main__':
    # if platform == 'darwin':
    #     assert len(sys.argv) == 2, 'why so many?'

    #     url = sys.argv[-1]
    #     print(sys.argv)
    #     make_and_move(url)
    # else:
    #     print('this tool requires macOS')

def add_arguments_to_parser(parser) -> None:
    parser.add_argument('url', help='youtube video url')
    parser.add_argument('-n', '--name', help='name of the rendered auido file')
    parser.add_argument('--album', help='album name')
    parser.add_argument('--artist', help='artist name')
    parser.add_argument(
        '-l', '--location',
        default=(
            os.path.join(
                os.path.expanduser('~'),
                'Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/'
            ) if platform == 'darwin'
            else './'
        ) # ! Need to modify path on macOS in the presense of artist and / or album names
    )

    # artwork source arguments
    source_group = parser.add_mutually_exclusive_group()
    # use from_google as default if google credentials are available else instagram
    source_group.add_argument('-g', '--google', action='store_true')
    source_group.add_argument('-i', '--ig-username', help='Add instagram username for artwork')
    source_group.add_argument('-u', '--art-url', help='Add artwork url')
    source_group.add_argument('--local', help='Add local artwork path')

def main(args: list[str]) -> None:
    parser = argparse.ArgumentParser(
        description=
            """download and configure audio file that's """
            """added to your local apple music library """
            """if your platform is macOS"""
    )
    add_arguments_to_parser(parser)
    args = parser.parse_args(args)

    default_filename, video_title = grab_music(args.url)
    # * default_filename is just a polished version of the video_title
    artwork_search_str = extract_search_str(video_title, args)
    """
    Next steps:
        Check if google credentials are available.
            then, use artwork_search_str to search for the artwork
            otherwise, make source_group required.
    """

def extract_artwork_src(args):
    pass

def extract_search_str(video_title, args):
    """extract_search_str extracts the string used to search artwork

    exploits the name, album and artist to find artwork

    :param video_title: the youtube video title
    :param args: the parser object potentially containing name, album and artist
    :return: artwork search str
    """
    audio_filename, album, artist = \
        args.name, args.album, args.artist

    title = audio_filename if audio_filename is not None \
        else video_title
    rest = ' '.join(filter([album, artist], lambda x : x is not None))
    return f'{title} {rest}'