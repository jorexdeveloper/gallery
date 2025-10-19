import flask
import typing


CONFIG_FILE = "config.py"
"""The configuration file for new app instances."""


def create_app(
        *, mapping: typing.Mapping[str, typing.Any] | None = None) -> flask.Flask:
    """Create a new app instance.

    Args:
        mapping (typing.Mapping[str, typing.Any] | None, optional): If not `None`, load the app configuration from mapping, otherwise load configuration from `CONFIG_FILE`. Defaults to `None`.

    Returns:
        flask.Flask: The created app instance.
    """

    app = flask.Flask(__name__)
    # app.logger.info("Created new app instance.")

    if mapping:
        # app.logger.info("Loading configuration from mapping.")
        app.config.from_mapping(mapping)
    else:
        # app.logger.info(
        #     "Loading configuration from python file: '%s'.",
        #     CONFIG_FILE)
        app.config.from_pyfile(CONFIG_FILE)

    try:
        # app.logger.info("Loading gallery data.")
        gallery_data = load_gallery_data()
    except Exception as e:
        # app.logger.exception("Exception while loading gallery data: %s", e)
        gallery_data = {"directories": {}, "media_files": set()}

    app.config.from_mapping(GALLERY_DATA=gallery_data)

    from . import routes

    # app.logger.info("Registering Blueprints.")
    app.register_blueprint(routes.DEFAULT_BLUEPRINT)

    return app


def load_gallery_data(force_new: bool = False) -> dict:
    """Load the gallery data from the manifest information.

    Args:
        force_new (bool, optional): If `True`, generate new manifest information. Defaults to `False`.

    Returns:
        dict: The gallery data.
    """

    from . import manifest
    from . import models

    import os

    gallery_info = manifest.get_manifest(force_new=force_new)
    gallery_data = {
        "directories": {},
        "media_files": set(gallery_info.get("media_files")),
        "thumbnails": set(gallery_info.get("thumbnails"))}

    for path, info in gallery_info.get("directories").items():
        if path:
            path_parts = path.split(os.sep)
            breadcrumbs = [(p, '/'.join(path_parts[:i + 1]))
                           for i, p in enumerate(path_parts)]
        else:
            breadcrumbs = []

        media = [
            models.MediaItem(
                path=p) for p in info["media"]]

        subdirs = [
            models.DirectoryItem(
                path=p,
                count=d["count"],
                thumbnail=models.MediaItem(
                    d["thumbnail"])) for p,
            d in info["subdirs"].items()]

        gallery_data["directories"][path] = {
            "breadcrumbs": breadcrumbs,
            "items": media + subdirs,
            "count": len(media) + len(subdirs)}

    return gallery_data
