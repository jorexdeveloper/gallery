from . import config
from . import utils

import json
import os


def _gen_manifest(path: str = config.MEDIA_DIR) -> dict:
    """Return new manifest information.

    Args:
        path (str, optional): The path to the media directory. Defaults to `config.MEDIA_DIR`.

    Returns:
        dict: The manifest information.
    """

    abs_path, directories, media_files = utils.get_abs_path(path), {}, []

    if os.path.isdir(abs_path):
        for root, dirs, files in os.walk(config.MEDIA_DIR, topdown=False):
            root_path = os.path.relpath(root, config.MEDIA_DIR)

            if root_path == '.':
                root_path = ''

            root_media = []
            for file in sorted(files):
                file_path = os.path.join(root_path, file)

                if utils.is_media(file_path):
                    root_media.append(file_path)
                    media_files.append(file_path)

            root_count = len(root_media)
            root_thumbnail = root_media[0] if root_count else None

            root_dir_data = {}
            for dir in sorted(dirs):
                dir_path = os.path.join(root_path, dir)

                if dir_path in directories:
                    root_count += directories[dir_path]["count"]

                    if not root_thumbnail:
                        root_thumbnail = directories[dir_path]["thumbnail"]

                    root_dir_data[dir_path] = {
                        "thumbnail": directories[dir_path]["thumbnail"],
                        "count": directories[dir_path]["count"]
                    }

            if root_count:
                directories[root_path] = {
                    "media": root_media,
                    "subdirs": root_dir_data,
                    "thumbnail": root_thumbnail,
                    "count": root_count
                }

    elif utils.is_media(abs_path):
        rel_path = os.path.relpath(abs_path, config.MEDIA_DIR)

        directories[''] = {
            "media": [rel_path],
            "subdirs": {},
            "thumbnail": rel_path,
            "count": 1
        }

        media_files.append(rel_path)

    return {"directories": directories, "media_files": media_files}


def get_manifest(*, name: str = config.MANIFEST_NAME,
                 dir: str = config.MANIFEST_DIR, force_new: bool = False) -> dict:
    """Return the cached manifest information, or generate new information if it's absent.

    Args:
        name (str, optional): The name of the manifest file. Defaults to `config.MANIFEST_NAME`.
        dir (str, optional): The directory of the manifest file. Defaults to `config.MANIFEST_DIR`.
        force_new (bool, optional): If `True`, generate new manifest information. Defaults to `False`.

    Returns:
        dict: The manifest information.
    """

    if force_new:
        return _gen_manifest()

    try:
        with open(os.path.join(dir, name), 'r', encoding="utf-8") as f:
            manifest = json.load(f)
            return manifest

    except Exception:
        return _gen_manifest()


def export_manifest(
        manifest: dict, *, name: str = config.MANIFEST_NAME, dir: str = config.MANIFEST_DIR) -> None:
    """Export the manifest information to a JSON file.

    Args:
        manifest (dict): The manifest information.
        name (str, optional): The name of the manifest file. Defaults to `config.MANIFEST_NAME`.
        dir (str, optional): The directory in which to save the manifest file. Defaults to `config.MANIFEST_DIR`.
    """

    os.makedirs(dir, exist_ok=True)

    with open(os.path.join(dir, name), 'w', encoding="utf-8") as f:
        json.dump(manifest, f)


if __name__ == "__main__":
    export_manifest(
        get_manifest(force_new=True))
    print(f"{os.path.relpath(config.MANIFEST_PATH)} created successfully!")
