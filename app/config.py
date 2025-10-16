import dotenv
import os


# General

DOT_ENV_LOADED = dotenv.load_dotenv()
"""True if the dot env was loaded, False otherwise."""

# Media

media_dir = os.environ.get("MEDIA_DIR", "media")
MEDIA_DIR = os.path.realpath(media_dir)
"""The path to the media directory."""

image_exts = os.environ.get("IMAGE_EXTS", '')
IMAGE_EXTS = set(e.strip().lower()
                 for e in (image_exts.split(',') if image_exts else ''))
"""The allowed image extensions."""

video_exts = os.environ.get("VIDEO_EXTS", '')
VIDEO_EXTS = set(e.strip().lower()
                 for e in (video_exts.split(',') if video_exts else ''))
"""The allowed video extensions."""

MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS
"""The allowed media extensions."""

# Cache

cache_dir = os.environ.get("CACHE_DIR", ".cache")
CACHE_DIR = os.path.realpath(cache_dir)
"""The directory containing cache files."""

manifest_file = os.environ.get("MANIFEST_FILE", "manifest.json")
MANIFEST_FILE = manifest_file.strip()
"""The name of the manifest file."""

MANIFEST_PATH = os.path.join(CACHE_DIR, MANIFEST_FILE)
"""The path to the manifest file."""

THUMBNAILS_FILE = os.environ.get("THUMBNAILS_FILE", "thumbnails")
"""The name of the thumbnails directory."""

THUMBNAILS_DIR = os.path.join(CACHE_DIR, THUMBNAILS_FILE)
"""The path to the thumbnails directory."""

THUMBNAILS_EXT = os.environ.get("THUMBNAILS_EXT", ".webm")
"""The file extension of the thumbnails."""


def validate_config(*, strict=False) -> bool:
    """Validates all the configuration variables.

    Args:
        strict (bool, optional): If `True` checks for existence of files and directories. Defaults to `False`.

    Returns:
        bool: True if all configuration variables are set and not empty.
    """

    try:
        assert DOT_ENV_LOADED, "Dot env not loaded."

        assert MEDIA_DIR, "MEDIA_DIR not set."
        assert IMAGE_EXTS, "IMAGE_EXTS not set."
        assert VIDEO_EXTS, "VIDEO_EXTS not set."
        assert MEDIA_EXTS, "MEDIA_EXTS not set."

        assert CACHE_DIR, "CACHE_DIR not set."
        assert MANIFEST_FILE, "MANIFEST_FILE not set."
        assert MANIFEST_PATH, "MANIFEST_PATH not set."

        assert THUMBNAILS_FILE, "THUMBNAILS_FILE not set."
        assert THUMBNAILS_DIR, "THUMBNAILS_DIR not set."
        assert THUMBNAILS_EXT, "THUMBNAILS_EXT not set."

        if strict:
            assert os.path.isdir(MEDIA_DIR), "MEDIA_DIR does not exist"
            assert os.path.isdir(CACHE_DIR), "CACHE_DIR does not exist"
            assert os.path.isfile(
                MANIFEST_PATH), "MANIFEST_PATH does not exist."
            assert os.path.isdir(
                THUMBNAILS_DIR), "THUMBNAILS_DIR does not exist."

        return True

    except AssertionError:
        return False
