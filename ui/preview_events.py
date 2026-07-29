# ui/preview_events.py

from PySide6.QtCore import Qt


class PreviewEvents:
    """
    Handles preview mouse and keyboard input.

    Current controls:
        - Mouse wheel = zoom
        - Middle mouse = pan
        - R = reset view
    """

    def __init__(
        self,
        widget,
        project,
        scene,
        selection_controller,
        zoom_controller
    ):

        self.widget = widget

        self.project = project

        self.scene = scene

        self.selection = selection_controller

        self.zoom = zoom_controller


    # --------------------------------------------------
    # Mouse
    # --------------------------------------------------

    def mouse_press(
        self,
        event
    ):

        if (
            event.button()
            ==
            Qt.MiddleButton
        ):

            self.zoom.begin_pan(
                event.position().x(),
                event.position().y()
            )


    def mouse_move(
        self,
        event
    ):

        if self.zoom.panning:

            self.zoom.update_pan(
                event.position().x(),
                event.position().y()
            )

            self.widget.update()


    def mouse_release(
        self,
        event
    ):

        if (
            event.button()
            ==
            Qt.MiddleButton
        ):

            self.zoom.end_pan()


    # --------------------------------------------------
    # Wheel
    # --------------------------------------------------

    def wheel(
        self,
        event
    ):

        delta = (
            event.angleDelta()
            .y()
        )


        if delta > 0:

            self.zoom.zoom_in()

        else:

            self.zoom.zoom_out()


        self.widget.update()


    # --------------------------------------------------
    # Keyboard
    # --------------------------------------------------

    def key_press(
        self,
        event
    ):

        if event.key() == Qt.Key_R:

            self.zoom.reset_view()

            self.widget.update()