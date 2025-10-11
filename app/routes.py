import flask


DEFAULT_BLUEPRINT = flask.Blueprint("gallery", __name__)
"""The default blueprint for all app instances."""


def _abort(code: int) -> None:
    """Call flask.abort with the appropriate error message.

    Args:
        code (int): Status code.
    """

    match code:
        case 404:
            msg = "Resource Not Found."

        case _:
            msg = "An Unknown Error Occurred."

    flask.abort(code, msg)


@DEFAULT_BLUEPRINT.route("/")
def index() -> str:
    """Return the gallery index page.

    Returns:
        str: The rendered HTML for the index page.
    """

    return page(path='')


@DEFAULT_BLUEPRINT.route("/<path:path>/")
def page(path: str) -> str:
    """Return a gallery directory page.

    Args:
        path (str): The path to the directory.

    Returns:
        str: The rendered HTML for the directory page.
    """

    flask.current_app.logger.info(
        "Request for page: '%s'.",
        path or "index")

    data = flask.current_app.config["GALLERY_DATA"]["directories"].get(path)
    if data:
        flask.current_app.logger.info("Returning page: '%s'.", path)
        return flask.render_template(
            "index.html", breadcrumbs=data["breadcrumbs"], media=data["media"], subdirs=data["subdirs"])

    flask.current_app.logger.info("Page not found: '%s'.", path or "index")
    _abort(404)


@DEFAULT_BLUEPRINT.route("/media/<path:path>")
def media(path: str) -> flask.Response:
    """Return a gallery media file.

    Args:
        path (str): The path to the media file.

    Returns:
        str : The media file.
    """

    flask.current_app.logger.info(
        "Request for media file: '%s'.", path)

    data_path = path.rstrip('/')
    if data_path in flask.current_app.config["GALLERY_DATA"]["media_files"]:
        if path and path.endswith('/'):
            path = path.rstrip('/')

            flask.current_app.logger.info(
                "Redirecting to: '%s'.", path)
            return flask.current_app.redirect(
                flask.current_app.url_for("page", path=path))

        flask.current_app.logger.info("Returning media file: '%s'.", path)
        return flask.send_from_directory(
            flask.current_app.config["MEDIA_DIR"], path)

    flask.current_app.logger.info("Media file not found: '%s'.", path)
    _abort(404)
