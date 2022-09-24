# Third party imports
import validators
import youtube_dl as ydl

# local imports
from .utils.utils import assert_domain, sugar_filename, MP3_DIR


def validate_url(video_url: str) -> None:
    """validate_url validates the youtube url

    Ensures the following:
    - valid url
    - valid hostname: youtube

    :param video_url: string url
    """
    assert validators.url(video_url), f"Bad URL: {video_url}"
    assert_domain(video_url, 'youtube')

def grab_music(video_url: str) -> None:
    """grab an mp3 from the given youtube video_url

    :param video_url: youtube url string
    """
    validate_url(video_url)

    video_info = ydl.YoutubeDL().extract_info(
        url=video_url, download=False
    )

    filename = (f'./{MP3_DIR}/' +
        sugar_filename(video_info['title'], extension='.mp3'))
    video_options = {
        'format': 'bestaudio/best',
        'audioformat': 'mp3',
        'keepvideo': False,
        'quiet': True,
        'outtmpl': filename,
    }

    with ydl.YoutubeDL(video_options) as downloader:
        downloader.download([video_info['webpage_url']])

    return filename, video_info['title']