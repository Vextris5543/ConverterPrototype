# ui/timeline_widget.py

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)


class TimelineWidget(QWidget):
    """
    Video timeline controls.

    Includes:
        - Play
        - Pause
        - Frame seeking
        - Frame counter
    """

    playClicked = Signal()

    pauseClicked = Signal()

    seekRequested = Signal(int)

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

        self.frame_count = 0

        self.build_ui()

        self.connect_signals()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def build_ui(self):

        layout = QHBoxLayout(
            self
        )


        self.play_button = QPushButton(
            "Play"
        )

        layout.addWidget(
            self.play_button
        )


        self.pause_button = QPushButton(
            "Pause"
        )

        layout.addWidget(
            self.pause_button
        )


        self.slider = QSlider(
            Qt.Horizontal
        )

        self.slider.setMinimum(
            0
        )

        self.slider.setMaximum(
            0
        )

        layout.addWidget(
            self.slider,
            1
        )


        self.frame_label = QLabel(
            "0 / 0"
        )

        layout.addWidget(
            self.frame_label
        )

    # --------------------------------------------------
    # Signals
    # --------------------------------------------------

    def connect_signals(self):

        self.play_button.clicked.connect(
            self.playClicked.emit
        )

        self.pause_button.clicked.connect(
            self.pauseClicked.emit
        )

        self.slider.valueChanged.connect(
            self.seekRequested.emit
        )

    # --------------------------------------------------
    # Frame Count
    # --------------------------------------------------

    def set_frame_count(
        self,
        count
    ):

        self.frame_count = count

        self.slider.setMaximum(
            max(
                0,
                count - 1
            )
        )

        self.update_frame(
            0,
            count
        )

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update_frame(
        self,
        frame,
        total=None
    ):

        if total is not None:

            self.frame_count = total


        self.slider.blockSignals(
            True
        )

        self.slider.setValue(
            frame
        )

        self.slider.blockSignals(
            False
        )


        self.frame_label.setText(
            f"{frame} / {self.frame_count}"
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def current_frame(self):

        return self.slider.value()