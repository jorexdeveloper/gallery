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

# Manifest

manifest_dir = os.environ.get("MANIFEST_DIR", '.')
MANIFEST_DIR = os.path.realpath(manifest_dir)
"""The directory of the manifest file."""

manifest_file = os.environ.get("MANIFEST_NAME", "manifest.json")
MANIFEST_NAME = manifest_file.strip()
"""The name of the manifest file."""

MANIFEST_PATH = os.path.join(MANIFEST_DIR, MANIFEST_NAME)
"""The path to the manifest file."""


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

        assert MANIFEST_DIR, "MANIFEST_DIR not set."
        assert MANIFEST_NAME, "MANIFEST_NAME not set."
        assert MANIFEST_PATH, "MANIFEST_PATH not set."

        if strict:
            assert os.path.isdir(MEDIA_DIR), "MEDIA_DIR does not exist"
            assert os.path.isdir(MANIFEST_DIR), "MANIFEST_DIR does not exist"
            assert os.path.isfile(
                MANIFEST_PATH), "MANIFEST_PATH does not exist."

        return True

    except AssertionError:
        return False
