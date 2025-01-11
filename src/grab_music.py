# Std lib imports
from typing import Tuple

# Third party imports
import validators
from pytubefix import YouTube

# local imports
from .utils.utils import MP3_DIR, assert_domain, sugar_filename


def validate_url(video_url: str) -> None:
    """validate_url validates the youtube url

    Ensures the following:
    - valid url
    - valid hostname: youtube

    :param video_url: string url
    """
    assert validators.url(video_url), f"Bad URL: {video_url}"
    assert_domain(video_url, "youtube")


def grab_music(video_url: str) -> Tuple[str, str]:
    """grab an mp3 from the given youtube video_url

    :param video_url: youtube url string
    :return: music filename, music title
    """
    validate_url(video_url)

    video = (
        YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
        .streams.filter(only_audio=True)
        .first()
    )
    title = video.title
    filename = f"./{MP3_DIR}/" + sugar_filename(
        title, extension=".mp3"
    )

    try:
        video.download(
            output_path=f"./{MP3_DIR}/",
            filename=sugar_filename(title, extension=".mp3"),
        )
    except Exception as e:
        print(f"Download Error: {e}")

    return filename, title
