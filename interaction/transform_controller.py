# interaction/transform_controller.py

from PySide6.QtCore import QObject, Signal


class TransformController(QObject):
    """
    Handles DDS overlay transformations.

    Controls:
        - Position
        - Scale
        - Rotation
        - Reset
    """

    transformChanged = Signal()

    def __init__(self, project):

        super().__init__()

        self.project = project

    # --------------------------------------------------
    # Position
    # --------------------------------------------------

    def set_position(
        self,
        x,
        y
    ):

        if not self.project.has_dds:
            return

        mask = self.project.mask

        mask.capture_x = x
        mask.capture_y = y

        self.transformChanged.emit()

    def set_x(
        self,
        value
    ):

        if not self.project.has_dds:
            return

        self.project.mask.capture_x = value

        self.transformChanged.emit()

    def set_y(
        self,
        value
    ):

        if not self.project.has_dds:
            return

        self.project.mask.capture_y = value

        self.transformChanged.emit()

    # --------------------------------------------------
    # Scale
    # --------------------------------------------------

    def set_scale(
        self,
        value
    ):

        if not self.project.has_dds:
            return

        # Slider values are expected as percentages.
        #
        # 100 = original size
        # 200 = double size
        # 50  = half size

        self.project.mask.scale = (
            value / 100.0
        )

        self.transformChanged.emit()

    # --------------------------------------------------
    # Rotation
    # --------------------------------------------------

    def set_rotation(
        self,
        value
    ):

        if not self.project.has_dds:
            return

        self.project.mask.rotation = value

        self.transformChanged.emit()

    # --------------------------------------------------
    # Opacity
    # --------------------------------------------------

    def set_opacity(
        self,
        value
    ):

        self.project.overlay_opacity = (
            value / 100.0
        )

        self.transformChanged.emit()

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self):

        if not self.project.has_dds:
            return

        mask = self.project.mask

        mask.capture_x = 0
        mask.capture_y = 0

        mask.scale = 1.0

        mask.rotation = 0

        self.project.overlay_opacity = 0.5

        self.transformChanged.emit()