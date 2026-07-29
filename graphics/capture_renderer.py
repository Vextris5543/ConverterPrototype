# graphics/capture_renderer.py

from PySide6.QtCore import QRectF
from PySide6.QtGui import (
    QColor,
    QPen,
)


class CaptureRenderer:
    """
    Draws the active capture area.

    This is the area of the video that will be
    copied into the DDS output.
    """

    def __init__(self, project):

        self.project = project

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def draw(
        self,
        painter,
        video_renderer
    ):

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


        rect = QRectF(
            x,
            y,
            w,
            h
        )


        painter.save()


        pen = QPen(
            QColor(
                255,
                255,
                255
            )
        )

        pen.setWidth(
            2
        )

        painter.setPen(
            pen
        )


        painter.drawRect(
            rect
        )


        painter.restore()

    # --------------------------------------------------
    # Hit Test
    # --------------------------------------------------

    def contains(
        self,
        x,
        y
    ):

        if not self.project.has_dds:
            return False


        mask = self.project.mask


        # Convert capture rectangle to screen space

        sx, sy = self.project.video_player.get_size()


        return (
            0 <= x <= sx and
            0 <= y <= sy
        )