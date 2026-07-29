from PySide6.QtCore import QRectF

from PySide6.QtGui import (
    QPainter,
)


class PreviewScene:

    def __init__(
        self,
        project
    ):

        self.project = project

        self.video_pixmap = None

        self.dds_pixmap = None

        self.selected = False



    def set_video(
        self,
        pixmap
    ):

        self.video_pixmap = pixmap



    def set_dds(
        self,
        pixmap
    ):

        self.dds_pixmap = pixmap



    def select_dds(
        self,
        state=True
    ):

        self.selected = state



    def draw(
        self,
        painter,
        widget
    ):

        painter.setRenderHint(
            QPainter.Antialiasing,
            True
        )


        # -------------------------
        # VIDEO
        # -------------------------

        if self.video_pixmap:

            painter.drawPixmap(
                QRectF(
                    0,
                    0,
                    widget.width(),
                    widget.height()
                ),
                self.video_pixmap,
                QRectF(
                    0,
                    0,
                    self.video_pixmap.width(),
                    self.video_pixmap.height()
                )
            )



        # -------------------------
        # DDS TEMPLATE
        # -------------------------

        if self.dds_pixmap:

            mask = getattr(
                self.project,
                "mask",
                None
            )


            if mask:

                scale = getattr(
                    mask,
                    "scale",
                    1.0
                )


                x = getattr(
                    mask,
                    "capture_x",
                    0
                )


                y = getattr(
                    mask,
                    "capture_y",
                    0
                )


                frame_x = getattr(
                    mask,
                    "frame_x",
                    0
                )


                frame_y = getattr(
                    mask,
                    "frame_y",
                    0
                )


                width = getattr(
                    mask,
                    "capture_width",
                    self.dds_pixmap.width()
                )


                height = getattr(
                    mask,
                    "capture_height",
                    self.dds_pixmap.height()
                )


                # source rectangle inside DDS
                source = QRectF(
                    frame_x,
                    frame_y,
                    width,
                    height
                )


                # destination on preview
                target = QRectF(
                    x,
                    y,
                    width * scale,
                    height * scale
                )


                painter.save()

                center_x = target.center().x()
                center_y = target.center().y()

                painter.translate(center_x, center_y)
                painter.rotate(mask.rotation)
                painter.translate(-center_x, -center_y)

                painter.drawPixmap(
                    target,
                    self.dds_pixmap,
                    source
                )

                painter.restore()


            else:

                painter.drawPixmap(
                    QRectF(
                        0,
                        0,
                        self.dds_pixmap.width(),
                        self.dds_pixmap.height()
                    ),
                    self.dds_pixmap
                )