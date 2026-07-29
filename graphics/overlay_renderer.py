# graphics/overlay_renderer.py

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter


class OverlayRenderer:
    """
    Draws the DDS template overlay on top of the video.

    The DDS remains its original dimensions.
    The transform only affects preview positioning.
    """

    def __init__(self, project):

        self.project = project

        self.pixmap = None

    # --------------------------------------------------
    # Set Image
    # --------------------------------------------------

    def set_pixmap(
        self,
        pixmap
    ):

        self.pixmap = pixmap

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def draw(
        self,
        painter,
        video_renderer
    ):

        if self.pixmap is None:
            return

        if not self.project.has_dds:
            return


        mask = self.project.mask


        x, y = video_renderer.image_to_screen(
            mask.capture_x,
            mask.capture_y
        )


        w, h = video_renderer.image_to_screen_size(
            mask.capture_width,
            mask.capture_height
        )


        scale = mask.scale


        w *= scale
        h *= scale


        rect = QRectF(
            x,
            y,
            w,
            h
        )


        painter.save()


        painter.setOpacity(
            self.project.overlay_opacity
        )


        painter.drawPixmap(
            rect,
            self.pixmap,
            self.pixmap.rect()
        )


        painter.restore()