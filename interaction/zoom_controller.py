# interaction/zoom_controller.py

from PySide6.QtCore import QObject, Signal


class ZoomController(QObject):
    """
    Handles preview zoom and panning.

    Controls:
        - Zoom in/out
        - Reset view
        - Middle mouse pan
    """

    zoomChanged = Signal()

    def __init__(
        self,
        project
    ):

        super().__init__()

        self.project = project


        self.pan_start_x = 0

        self.pan_start_y = 0

        self.start_pan_x = 0

        self.start_pan_y = 0

        self.panning = False


    # --------------------------------------------------
    # Zoom
    # --------------------------------------------------

    def zoom_in(self):

        self.project.zoom *= 1.1

        self.project.zoom = min(
            self.project.zoom,
            10.0
        )

        self.zoomChanged.emit()


    def zoom_out(self):

        self.project.zoom /= 1.1

        self.project.zoom = max(
            self.project.zoom,
            0.1
        )

        self.zoomChanged.emit()


    def set_zoom(
        self,
        value
    ):

        self.project.zoom = max(
            0.1,
            min(
                value,
                10.0
            )
        )

        self.zoomChanged.emit()


    # --------------------------------------------------
    # Pan
    # --------------------------------------------------

    def begin_pan(
        self,
        x,
        y
    ):

        self.panning = True


        self.pan_start_x = x

        self.pan_start_y = y


        self.start_pan_x = (
            self.project.pan_x
        )

        self.start_pan_y = (
            self.project.pan_y
        )


    def update_pan(
        self,
        x,
        y
    ):

        if not self.panning:

            return


        dx = (
            x
            -
            self.pan_start_x
        )

        dy = (
            y
            -
            self.pan_start_y
        )


        self.project.pan_x = (
            self.start_pan_x
            +
            dx
        )

        self.project.pan_y = (
            self.start_pan_y
            +
            dy
        )


        self.zoomChanged.emit()


    def end_pan(self):

        self.panning = False


    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset_view(self):

        self.project.zoom = 1.0

        self.project.pan_x = 0

        self.project.pan_y = 0


        self.zoomChanged.emit()