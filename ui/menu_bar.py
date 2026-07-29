# ui/menu_bar.py

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QMenuBar,
    QMenu,
    QFileDialog,
)


class MenuBar(QMenuBar):
    """
    Application menu bar.

    Provides:
        - Open video
        - Open DDS
        - Export
        - Project save/load
        - Reset options
    """

    openVideo = Signal()

    openDDS = Signal()

    exportDDS = Signal()

    saveProject = Signal()

    loadProject = Signal()

    resetView = Signal()

    resetTransform = Signal()

    exitProgram = Signal()

    # --------------------------------------------------
    # Init
    # --------------------------------------------------

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.build_menu()

    # --------------------------------------------------
    # Menu
    # --------------------------------------------------

    def build_menu(self):

        file_menu = QMenu(
            "File",
            self
        )

        view_menu = QMenu(
            "View",
            self
        )

        tools_menu = QMenu(
            "Tools",
            self
        )


        # File

        open_video = file_menu.addAction(
            "Open Video"
        )

        open_dds = file_menu.addAction(
            "Open DDS Template"
        )

        file_menu.addSeparator()


        export = file_menu.addAction(
            "Export DDS Sequence"
        )

        file_menu.addSeparator()


        save = file_menu.addAction(
            "Save Project"
        )

        load = file_menu.addAction(
            "Load Project"
        )

        file_menu.addSeparator()


        exit_action = file_menu.addAction(
            "Exit"
        )


        # View

        reset_view = view_menu.addAction(
            "Reset View"
        )


        # Tools

        reset_transform = tools_menu.addAction(
            "Reset Transform"
        )


        # Add menus

        self.addMenu(
            file_menu
        )

        self.addMenu(
            view_menu
        )

        self.addMenu(
            tools_menu
        )


        # Connections

        open_video.triggered.connect(
            self.openVideo.emit
        )

        open_dds.triggered.connect(
            self.openDDS.emit
        )

        export.triggered.connect(
            self.exportDDS.emit
        )

        save.triggered.connect(
            self.saveProject.emit
        )

        load.triggered.connect(
            self.loadProject.emit
        )

        reset_view.triggered.connect(
            self.resetView.emit
        )

        reset_transform.triggered.connect(
            self.resetTransform.emit
        )

        exit_action.triggered.connect(
            self.exitProgram.emit
        )