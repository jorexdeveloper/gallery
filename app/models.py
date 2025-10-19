from . import config

import dataclasses
import os


@dataclasses.dataclass
class MediaItem:
    """Represents a media item.

    Attributes:
        path (str): The path to the media item.
        name (str, optional): The name of the media item.
        type (str, optional): The type of the media item.
        ext (str, optional): The extension of the media item.
    """

    path: str
    """The path to the media item."""

    name: str = ""
    """The name of the media item."""

    type: str = ""
    """The type of the media item."""

    ext: str = ""
    """The extension of the media item."""

    thumb: str = ""
    """The path to the thumbnail image of the media item."""

    def __post_init__(self):
        """Set optional attributes."""

        info = os.path.splitext(self.path)

        if not self.name:
            self.name = os.path.basename(info[0])

        if not self.ext:
            self.ext = info[1]

        if not self.type:
            if self.ext in config.VIDEO_EXTS:
                self.type = "video"
            elif self.ext in config.IMAGE_EXTS:
                self.type = "image"

        if not self.thumb:
            self.thumb = os.path.join(info[0] + config.THUMBNAILS_EXT)


@dataclasses.dataclass
class DirectoryItem:
    """Represents a directory item.

    Attributes:
        path (str) : The path to the directory item.
        count (str) : The number of media items in the directory.
        thumbnail (MediaItem) : The path to the thumbnail of the directory.
        name (str, optional): The name of the directory item.
    """

    path: str
    """The path to the directory item."""

    count: int
    """The number of media items in the directory."""

    thumbnail: MediaItem
    """The path to the thumbnail of the directory."""

    name: str = ""
    """The name of the directory item."""

    def __post_init__(self):
        """Set optional attributes."""

        if not self.name:
            self.name = os.path.basename(self.path)
