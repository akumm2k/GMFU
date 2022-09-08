import validators
import youtube_dl as ydl
import json
from utils import assert_domain


def validate_url(video_url: str) -> None:
    """validate_url validates the youtube url

    Ensures the following:
    - valid url
    - valid hostname: youtube

    :param video_url: string url
    """
    assert validators.url(video_url), f"Bad URL: {video_url}" 
    assert_domain(video_url, 'youtube')

def sugar_filename(sour_filename: str) -> str:
    """sugar_filename polishes up the video filename

    :param sour_filename: video filename string
    :return: tweaked video filename
    """
    return (sour_filename.strip()
        .replace(' ', '-')
        .replace('/', '-')
    ) + '.mp3'

def grab_video(video_url: str) -> None:
    """grab an mp3 from the given youtube video_url

    :param video_url: youtube url string
    """
    validate_url(video_url)

    video_info = ydl.YoutubeDL().extract_info(
        url=video_url, download=False
    )

    filename = sugar_filename(video_info['title'])
    video_options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'quiet': True,
        'outtmpl': filename,
    }

    with ydl.YoutubeDL(video_options) as downloader:
        downloader.download([video_info['webpage_url']])