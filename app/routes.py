import flask


DEFAULT_BLUEPRINT = flask.Blueprint("gallery", __name__)
"""The default blueprint for all app instances."""

ITEMS_PER_PAGE = 10
"""The number of items to show on a single page."""


def _abort(code: int) -> None:
    """Call flask.abort with the appropriate error message.

    Args:
        code (int): Status code.
    """

    match code:
        case 400:
            msg = "Bad Request."
        case 404:
            msg = "Resource Not Found."
        case _:
            msg = "An Unknown Error Occurred."

    flask.abort(code, msg)


@DEFAULT_BLUEPRINT.route("/")
def index() -> str:
    """Return the index page.

    Returns:
        str: The rendered HTML for the index page.
    """

    return path(path='')


@DEFAULT_BLUEPRINT.route("/<path:path>/")
def path(path: str) -> str:
    """Return the main directory page.

    Args:
        path (str): The path to the directory.

    Returns:
        str: The rendered HTML for the directory page.
    """

    # flask.current_app.logger.info(
    #     "Request for main page of %s.",
    #     path or "index")

    # flask.current_app.logger.info(
    #     "Returning main page of %s.",
    #     path or "index")

    data = flask.current_app.config["GALLERY_DATA"]["directories"].get(path)
    if data:
        return flask.render_template(
            "index.html", breadcrumbs=data["breadcrumbs"], path=path, items=[], last=data["count"] <= 0)
    elif path == '':
        return flask.render_template(
            "index.html", breadcrumbs=[], path=path, items=[], last=data["count"] <= 0)

    # flask.current_app.logger.info("Path not found: '%s'.", path or "index")
    _abort(404)


@DEFAULT_BLUEPRINT.route("/pages")
def pages():
    """Return a gallery page.

    Returns:
        str: The rendered HTML for the gallery page.
    """

    path = flask.request.args.get("path", '')
    page = flask.request.args.get("page", '1')
    recurse = flask.request.args.get("recurse", '')

    # flask.current_app.logger.info(
    #     "Request for page %s of %s.",
    #     page,
    #     path or "index")

    try:
        page = int(page)
    except ValueError:
        # flask.current_app.logger.info("Invalid page number: '%s'.", page)
        _abort(400)

    data = flask.current_app.config["GALLERY_DATA"]["directories"][path]

    if not data:
        # flask.current_app.logger.info("Path not found: '%s'.", path or
        # "index")
        _abort(404)

    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    if recurse:
        items = []

        def _recurse(item_list):
            for item in item_list:
                if item.type == "directory":
                    _recurse(
                        flask.current_app.config["GALLERY_DATA"]["directories"][item.path]["items"])
                else:
                    items.append(item)

        _recurse(data["items"])

        last = len(items) <= end
        items = items[start:end]

        # flask.current_app.logger.info(
        #     "Returning page %d of %s.", page, path or "index")
        return flask.render_template(
            "index.html", path=path, items=items, last=last)
    else:
        items = data["items"][start:end]
        last = data["count"] <= end

        if items:
            # flask.current_app.logger.info(
            #     "Returning page %d of %s.", page, path or "index")
            return flask.render_template(
                "index.html", path=path, items=items, last=last)

    # flask.current_app.logger.info(
    #     "Page %d not found for %s.", page, path or "index")
    _abort(404)


@DEFAULT_BLUEPRINT.route("/media/<path:path>")
def media(path: str) -> flask.Response:
    """Return a media file.

    Args:
        path (str): The path to the media file.

    Returns:
        str : The media file.
    """

    # flask.current_app.logger.info(
    #     "Request for media file: '%s'.", path)

    data_path = path.rstrip('/')
    if data_path in flask.current_app.config["GALLERY_DATA"]["media_files"]:
        if path and path.endswith('/'):
            path = path.rstrip('/')

            # flask.current_app.logger.info(
            #     "Redirecting to: '%s'.", path)
            return flask.current_app.redirect(
                flask.current_app.url_for("page", path=path))

        # flask.current_app.logger.info("Returning media file: '%s'.", path)
        return flask.send_from_directory(
            flask.current_app.config["MEDIA_DIR"], path)

    # flask.current_app.logger.info("Media file not found: '%s'.", path)
    _abort(404)


@DEFAULT_BLUEPRINT.route("/thumbnails/<path:path>")
def thumbnails(path: str) -> flask.Response:
    """Return a thumbnail file.

    Args:
        path (str): The path to the thumbnail file.

    Returns:
        str : The thumbnail file.
    """

    # flask.current_app.logger.info(
    #     "Request for thumbnail file: '%s'.", path)

    data_path = path.rstrip('/')
    if data_path in flask.current_app.config["GALLERY_DATA"]["thumbnails"]:
        if path and path.endswith('/'):
            path = path.rstrip('/')

            # flask.current_app.logger.info(
            #     "Redirecting to: '%s'.", path)
            return flask.current_app.redirect(
                flask.current_app.url_for("page", path=path))

        # flask.current_app.logger.info("Returning thumbnail file: '%s'.", path)
        return flask.send_from_directory(
            flask.current_app.config["THUMBNAILS_DIR"], path)

    # flask.current_app.logger.info("Thumbnail not found: '%s'.", path)
    _abort(404)
