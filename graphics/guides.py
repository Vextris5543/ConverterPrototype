# graphics/guides.py

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QPen,
)


class Guides:
    """
    Draws helper guides over the preview.

    Current:
        - Center lines

    Future:
        - Grid
        - Safe zones
        - Alignment snapping
    """

    def __init__(self):

        self.enabled = True

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def draw(
        self,
        painter,
        rect
    ):

        if not self.enabled:
            return


        painter.save()


        pen = QPen(
            QColor(
                180,
                180,
                180
            )
        )

        pen.setStyle(
            Qt.DashLine
        )

        pen.setWidth(
            1
        )


        painter.setPen(
            pen
        )


        center_x = (
            rect.x()
            +
            rect.width() / 2
        )


        center_y = (
            rect.y()
            +
            rect.height() / 2
        )


        painter.drawLine(
            center_x,
            rect.top(),
            center_x,
            rect.bottom()
        )


        painter.drawLine(
            rect.left(),
            center_y,
            rect.right(),
            center_y
        )


        painter.restore()