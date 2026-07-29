# ui/transform_panel.py

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider,
    QPushButton,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)


class TransformPanel(QWidget):
    """
    DDS transform controls.

    Controls:
        - X position
        - Y position
        - Scale
        - Rotation
        - Overlay opacity
        - Reset
    """

    xChanged = Signal(int)

    yChanged = Signal(int)

    scaleChanged = Signal(int)

    rotationChanged = Signal(int)

    opacityChanged = Signal(int)

    resetClicked = Signal()

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

        self.build_ui()

        self.connect_signals()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout(
            self
        )


        # X

        layout.addWidget(
            QLabel(
                "X Position"
            )
        )

        self.x_slider = QSlider(
            Qt.Horizontal
        )

        self.x_slider.setRange(
            -500,
            500
        )

        layout.addWidget(
            self.x_slider
        )


        # Y

        layout.addWidget(
            QLabel(
                "Y Position"
            )
        )

        self.y_slider = QSlider(
            Qt.Horizontal
        )

        self.y_slider.setRange(
            -500,
            500
        )

        layout.addWidget(
            self.y_slider
        )


        # Scale

        layout.addWidget(
            QLabel(
                "Scale"
            )
        )

        self.scale_slider = QSlider(
            Qt.Horizontal
        )

        self.scale_slider.setRange(
            10,
            400
        )

        self.scale_slider.setValue(
            100
        )

        layout.addWidget(
            self.scale_slider
        )


        # Rotation

        layout.addWidget(
            QLabel(
                "Rotation"
            )
        )

        self.rotation_slider = QSlider(
            Qt.Horizontal
        )

        self.rotation_slider.setRange(
            -180,
            180
        )

        layout.addWidget(
            self.rotation_slider
        )


        # Opacity

        layout.addWidget(
            QLabel(
                "Overlay Opacity"
            )
        )

        self.opacity_slider = QSlider(
            Qt.Horizontal
        )

        self.opacity_slider.setRange(
            0,
            100
        )

        self.opacity_slider.setValue(
            50
        )

        layout.addWidget(
            self.opacity_slider
        )


        # Reset

        self.reset_button = QPushButton(
            "Reset Transform"
        )

        layout.addWidget(
            self.reset_button
        )


        layout.addStretch()

    # --------------------------------------------------
    # Signals
    # --------------------------------------------------

    def connect_signals(self):

        self.x_slider.valueChanged.connect(
            self.xChanged.emit
        )

        self.y_slider.valueChanged.connect(
            self.yChanged.emit
        )

        self.scale_slider.valueChanged.connect(
            self.scaleChanged.emit
        )

        self.rotation_slider.valueChanged.connect(
            self.rotationChanged.emit
        )

        self.opacity_slider.valueChanged.connect(
            self.opacityChanged.emit
        )

        self.reset_button.clicked.connect(
            self.resetClicked.emit
        )

    # --------------------------------------------------
    # Values
    # --------------------------------------------------

    def set_values(
        self,
        x,
        y,
        scale,
        rotation,
        opacity
    ):

        self.x_slider.blockSignals(
            True
        )

        self.y_slider.blockSignals(
            True
        )

        self.scale_slider.blockSignals(
            True
        )

        self.rotation_slider.blockSignals(
            True
        )

        self.opacity_slider.blockSignals(
            True
        )


        self.x_slider.setValue(
            int(x)
        )

        self.y_slider.setValue(
            int(y)
        )

        self.scale_slider.setValue(
            int(scale * 100)
        )

        self.rotation_slider.setValue(
            int(rotation)
        )

        self.opacity_slider.setValue(
            int(opacity * 100)
        )


        self.x_slider.blockSignals(
            False
        )

        self.y_slider.blockSignals(
            False
        )

        self.scale_slider.blockSignals(
            False
        )

        self.rotation_slider.blockSignals(
            False
        )

        self.opacity_slider.blockSignals(
            False
        )