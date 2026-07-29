# graphics/video_renderer.py

from PySide6.QtGui import QPixmap

from core.image_converter import ImageConverter


class VideoRenderer:
    """
    Converts video frames into preview-ready pixmaps.
    """

    def __init__(
        self
    ):

        self.current_pixmap = None


    # --------------------------------------------------
    # Render Frame
    # --------------------------------------------------

    def render(
        self,
        frame
    ):

        if frame is None:

            self.current_pixmap = None

            return None


        self.current_pixmap = (
            ImageConverter.cv_to_pixmap(
                frame
            )
        )


        return self.current_pixmap


    # --------------------------------------------------
    # Access
    # --------------------------------------------------

    def pixmap(
        self
    ):

        return self.current_pixmap


    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    def clear(
        self
    ):

        self.current_pixmap = None