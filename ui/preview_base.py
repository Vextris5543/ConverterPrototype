# ui/preview_base.py

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter


class PreviewBase:
    """
    Shared preview painting helper.
    """

    @staticmethod
    def paint(
        widget,
        event,
        scene
    ):

        painter = QPainter(
            widget
        )

        try:

            painter.setRenderHint(
                QPainter.SmoothPixmapTransform,
                True
            )


            painter.fillRect(
                widget.rect(),
                QColor(
                    25,
                    25,
                    25
                )
            )


            scene.draw(
                painter,
                widget
            )


            if (
                scene.video_pixmap is None
                and
                scene.dds_pixmap is None
            ):

                painter.setPen(
                    QColor(
                        220,
                        220,
                        220
                    )
                )


                painter.drawText(
                    widget.rect(),
                    Qt.AlignCenter,
                    (
                        "Drop video here\n\n"
                        "Drop DDS here"
                    )
                )


        finally:

            if painter.isActive():

                painter.end()