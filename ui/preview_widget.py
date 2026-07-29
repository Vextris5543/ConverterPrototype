from PySide6.QtWidgets import QWidget

from PySide6.QtCore import (
    Qt,
    Signal,
    QPointF,
)

from PySide6.QtGui import QPainter

from graphics.preview_scene import PreviewScene
from ui.preview_loader import PreviewLoader



class PreviewWidget(QWidget):

    videoDropped = Signal(str)
    ddsDropped = Signal(str)



    def __init__(
        self,
        project,
        parent=None
    ):

        super().__init__(parent)

        self.project = project


        self.scene = PreviewScene(
            project
        )


        self.loader = PreviewLoader(
            project,
            self.scene
        )


        self.dragging = False
        self.resizing = False


        self.drag_start = QPointF()

        self.resize_start = QPointF()

        self.start_scale = 1.0


        self.setAcceptDrops(True)

        self.setMouseTracking(True)



    def set_frame(
        self,
        frame
    ):

        self.loader.set_frame(
            frame
        )

        self.update()



    def set_dds(
        self,
        path
    ):

        result = self.loader.set_dds(
            path
        )


        self.scene.select_dds(
            True
        )


        self.update()


        return result



    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )


        self.scene.draw(
            painter,
            self
        )


        painter.end()



    def get_dds_rect(
        self
    ):

        mask = getattr(
            self.project,
            "mask",
            None
        )


        if mask is None:

            return None


        dds = self.scene.dds_pixmap


        if dds is None:

            return None



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


        width = getattr(
            mask,
            "capture_width",
            dds.width()
        )


        height = getattr(
            mask,
            "capture_height",
            dds.height()
        )


        return (
            x,
            y,
            width * scale,
            height * scale
        )



    def mousePressEvent(
        self,
        event
    ):

        if event.button() != Qt.LeftButton:

            return



        rect = self.get_dds_rect()


        if rect is None:

            return



        x, y, w, h = rect


        px = event.position().x()

        py = event.position().y()



        # Resize handle
        if (
            px >= x + w - 30
            and
            py >= y + h - 30
        ):

            self.resizing = True


            self.resize_start = event.position()


            self.start_scale = getattr(
                self.project.mask,
                "scale",
                1.0
            )


            return



        # Move template
        if (
            x <= px <= x + w
            and
            y <= py <= y + h
        ):

            self.dragging = True


            self.drag_start = event.position()



    def mouseMoveEvent(
        self,
        event
    ):

        mask = getattr(
            self.project,
            "mask",
            None
        )


        if mask is None:

            return



        # -------------------------
        # RESIZE
        # -------------------------

        if self.resizing:


            delta = (
                event.position().x()
                -
                self.resize_start.x()
            )


            mask.scale = max(
                0.05,
                self.start_scale + (delta / 300)
            )


            self.update()


            return



        # -------------------------
        # MOVE / ROTATE
        # -------------------------

        if self.dragging:

            delta = (
                event.position()
                -
                self.drag_start
            )

            # Ctrl + Drag = rotate
            if event.modifiers() & Qt.ControlModifier:

                mask.rotation += delta.x() * 0.5

                # Clamp rotation
                mask.rotation = max(
                    -180.0,
                    min(
                        180.0,
                        mask.rotation
                    )
                )

            # Normal drag = move
            else:

                mask.capture_x += delta.x()

                mask.capture_y += delta.y()

            self.drag_start = event.position()

            self.update()



    def mouseReleaseEvent(
        self,
        event
    ):

        if event.button() == Qt.LeftButton:

            self.dragging = False

            self.resizing = False



    def wheelEvent(
        self,
        event
    ):

        mask = getattr(
            self.project,
            "mask",
            None
        )


        if mask is None:

            return



        delta = event.angleDelta().y()


        if delta > 0:

            mask.scale += 0.05

        else:

            mask.scale -= 0.05



        mask.scale = max(
            0.05,
            mask.scale
        )


        self.update()



    def dragEnterEvent(
        self,
        event
    ):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()



    def dropEvent(
        self,
        event
    ):

        urls = event.mimeData().urls()


        if not urls:

            return


        path = urls[0].toLocalFile()



        if path.lower().endswith(
            (
                ".mp4",
                ".mov",
                ".avi",
                ".mkv"
            )
        ):

            self.videoDropped.emit(
                path
            )


        elif path.lower().endswith(
            ".dds"
        ):

            self.ddsDropped.emit(
                path
            )