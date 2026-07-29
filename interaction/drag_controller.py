# interaction/drag_controller.py

from PySide6.QtCore import QPointF


class DragController:
    """
    Handles dragging the capture rectangle.

    Coordinates are stored in image space, not screen space.
    """

    def __init__(self, project, video_renderer):

        self.project = project
        self.video_renderer = video_renderer

        self.dragging = False

        self.start_mouse = QPointF()
        self.start_capture = QPointF()

    # --------------------------------------------------
    # Mouse Press
    # --------------------------------------------------

    def mouse_press(self, x, y):

        if not self.project.has_dds:
            return False

        mask = self.project.mask

        sx, sy = self.video_renderer.image_to_screen(
            mask.capture_x,
            mask.capture_y
        )

        sw, sh = self.video_renderer.image_to_screen_size(
            mask.capture_width,
            mask.capture_height
        )

        if (
            sx <= x <= sx + sw and
            sy <= y <= sy + sh
        ):

            self.dragging = True

            self.start_mouse = QPointF(x, y)

            self.start_capture = QPointF(
                mask.capture_x,
                mask.capture_y
            )

            return True

        return False

    # --------------------------------------------------
    # Mouse Move
    # --------------------------------------------------

    def mouse_move(self, x, y):

        if not self.dragging:
            return False

        dx = x - self.start_mouse.x()
        dy = y - self.start_mouse.y()

        ix, iy = self.video_renderer.screen_to_image_size(
            dx,
            dy
        )

        mask = self.project.mask

        mask.capture_x = self.start_capture.x() + ix
        mask.capture_y = self.start_capture.y() + iy

        self.clamp()

        return True

    # --------------------------------------------------
    # Mouse Release
    # --------------------------------------------------

    def mouse_release(self):

        self.dragging = False

    # --------------------------------------------------
    # Clamp
    # --------------------------------------------------

    def clamp(self):

        player = self.project.video_player

        if player is None:
            return

        mask = self.project.mask

        max_x = max(
            0,
            player.width - mask.capture_width
        )

        max_y = max(
            0,
            player.height - mask.capture_height
        )

        mask.capture_x = max(
            0,
            min(mask.capture_x, max_x)
        )

        mask.capture_y = max(
            0,
            min(mask.capture_y, max_y)
        )

    # --------------------------------------------------
    # State
    # --------------------------------------------------

    @property
    def is_dragging(self):

        return self.dragging