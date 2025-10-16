from . import config
from . import models

import os


def is_media(path: str) -> bool:
    """Test whether a path is a media file.

    Args:
        path (str): The path to test.

    Returns:
        bool: True if the path is a media file, False otherwise.
    """

    return os.path.splitext(path)[1].lower() in config.MEDIA_EXTS


def get_abs_path(path: str) -> str:
    """Return the absolute path of a path if it's within `config.MEDIA_DIR`.

    Args:
        path (str): The path to test.

    Raises:
        ValueError: If the path is not within `config.MEDIA_DIR`.

    Returns:
        str: The absolute path.
    """

    abs_path = os.path.normpath(
        path if os.path.isabs(path) else os.path.abspath(
            os.path.join(config.MEDIA_DIR, path)))

    if os.path.commonpath([config.MEDIA_DIR, abs_path]) != config.MEDIA_DIR:
        raise ValueError(
            f"The path '{path}' not within the media directory '{config.MEDIA_DIR}'.")

    return abs_path


def get_rel_path(path: str) -> str:
    """Return the relative path of a path relative to `config.MEDIA_DIR`.

    Args:
        path (str): The path to test.

    Raises:
        ValueError: If the path is not within `config.MEDIA_DIR`.

    Returns:
        str: The relative path.
    """

    return os.path.relpath(get_abs_path(path), config.MEDIA_DIR)


def get_media_file(path: str = config.MEDIA_DIR) -> str | None:
    """Return the first media file in a path.

    This function is deprecated and nolonger used in the application due to performance reasons.

    Args:
        path (str, optional): The path to search. Defaults to `config.MEDIA_DIR`.

    Returns:
        str | None: The path to the first media file found, or None if no media file is found.
    """

    abs_path = get_abs_path(path)

    if os.path.isdir(abs_path):
        for root, dirs, files in os.walk(abs_path):
            for file in sorted(files):
                if is_media(os.path.join(root, file)):
                    return os.path.relpath(os.path.join(
                        root, file), config.MEDIA_DIR)

    elif is_media(abs_path):
        return os.path.relpath(abs_path, config.MEDIA_DIR)

    return None


def get_gallery_items(
        path: str = config.MEDIA_DIR) -> tuple[list[models.MediaItem], list[models.DirectoryItem]]:
    """Return all media items and directory items in a path.

    This function is deprecated and nolonger used in the application due to performance reasons.

    Args:
        path (str, optional): The path to search. Defaults to `config.MEDIA_DIR`.

    Returns:
        tuple[list[models.MediaItem], list[models.DirectoryItem]]: A tuple containing a list of media items and a list of directory items found.
    """

    abs_path, media, subdirs = get_abs_path(path), [], []

    if os.path.isdir(abs_path):
        for entry in sorted(os.scandir(abs_path), key=lambda e: e.name):
            rel_entry_path = os.path.relpath(entry.path, config.MEDIA_DIR)

            if entry.is_file() and is_media(entry.path):
                media.append(models.MediaItem(path=rel_entry_path))

            elif entry.is_dir():
                entry_thumbnail = get_media_file(entry.path)
                entry_item_count = sum(
                    1 for sub_entry in os.scandir(
                        entry.path) if (
                        sub_entry.is_file() and is_media(
                            sub_entry.path)) or get_media_file(
                        sub_entry.path))

                if entry_thumbnail:
                    subdirs.append(
                        models.DirectoryItem(
                            path=rel_entry_path,
                            count=entry_item_count,
                            thumbnail=models.MediaItem(
                                path=entry_thumbnail),
                        ))

    elif is_media(abs_path):
        media.append(
            models.MediaItem(
                name=os.path.basename(abs_path),
                path=os.path.relpath(
                    abs_path,
                    config.MEDIA_DIR)))

    return media, subdirs
