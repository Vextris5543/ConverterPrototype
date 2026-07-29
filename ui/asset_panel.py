# ui/asset_panel.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
)


class AssetPanel(QWidget):
    """
    Displays loaded project assets.

    Shows:
        - Video file
        - DDS template
    """

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.build_ui()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(
            self
        )


        layout.addWidget(
            QLabel(
                "Assets"
            )
        )


        self.asset_list = QListWidget()

        layout.addWidget(
            self.asset_list
        )


        layout.addStretch()

    # --------------------------------------------------
    # Assets
    # --------------------------------------------------

    def set_video(
        self,
        path
    ):

        self.remove_type(
            "Video:"
        )

        self.asset_list.addItem(
            f"Video: {path}"
        )


    def set_dds(
        self,
        path
    ):

        self.remove_type(
            "DDS:"
        )

        self.asset_list.addItem(
            f"DDS: {path}"
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def remove_type(
        self,
        prefix
    ):

        for i in range(
            self.asset_list.count() - 1,
            -1,
            -1
        ):

            item = (
                self.asset_list
                .item(i)
            )

            if item.text().startswith(
                prefix
            ):

                self.asset_list.takeItem(
                    i
                )

    def clear(self):

        self.asset_list.clear()