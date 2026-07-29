# interaction/selection_controller.py

from PySide6.QtCore import QObject, Signal


class SelectionController(QObject):
    """
    Handles selecting and storing the active preview item.

    Currently supports:
        - DDS overlay selection
        - Video selection
    """

    selectionChanged = Signal()

    def __init__(
        self,
        project,
        scene
    ):

        super().__init__()

        self.project = project

        self.scene = scene


        self.selected = None


    # --------------------------------------------------
    # Select
    # --------------------------------------------------

    def select(
        self,
        item
    ):

        self.selected = item

        self.selectionChanged.emit()


    def clear(
        self
    ):

        self.selected = None

        self.selectionChanged.emit()


    # --------------------------------------------------
    # Access
    # --------------------------------------------------

    def current(
        self
    ):

        return self.selected


    def has_selection(
        self
    ):

        return self.selected is not None


    # --------------------------------------------------
    # DDS Shortcut
    # --------------------------------------------------

    def select_mask(
        self
    ):

        if self.project.mask:

            self.select(
                self.project.mask
            )

        else:

            self.clear()