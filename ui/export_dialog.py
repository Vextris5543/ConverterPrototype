# ui/export_dialog.py

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QFileDialog,
)

from core.export_settings import ExportSettings



class ExportDialog(QDialog):
    """
    Export DDS sequence settings.

    Allows:
        - Start frame
        - End frame
        - Output folder
    """


    def __init__(
        self,
        frame_count,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.setWindowTitle(
            "Export DDS Sequence"
        )


        self.frame_count = frame_count


        self.output_folder = ""


        # Export settings object
        self.settings = ExportSettings()


        self.build_ui()



    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def build_ui(
        self
    ):


        layout = QVBoxLayout(
            self
        )


        # Start frame

        start_row = QHBoxLayout()


        start_row.addWidget(
            QLabel(
                "Start Frame:"
            )
        )


        self.start_frame = QSpinBox()


        self.start_frame.setRange(
            0,
            max(
                0,
                self.frame_count - 1
            )
        )


        start_row.addWidget(
            self.start_frame
        )


        layout.addLayout(
            start_row
        )



        # End frame

        end_row = QHBoxLayout()


        end_row.addWidget(
            QLabel(
                "End Frame:"
            )
        )


        self.end_frame = QSpinBox()


        self.end_frame.setRange(
            0,
            max(
                0,
                self.frame_count - 1
            )
        )


        self.end_frame.setValue(
            max(
                0,
                self.frame_count - 1
            )
        )


        end_row.addWidget(
            self.end_frame
        )


        layout.addLayout(
            end_row
        )



        # Folder

        folder_row = QHBoxLayout()


        self.folder_label = QLabel(
            "No output folder selected"
        )


        folder_button = QPushButton(
            "Choose Folder"
        )


        folder_button.clicked.connect(
            self.choose_folder
        )


        folder_row.addWidget(
            self.folder_label,
            1
        )


        folder_row.addWidget(
            folder_button
        )


        layout.addLayout(
            folder_row
        )



        # Buttons

        button_row = QHBoxLayout()


        export_button = QPushButton(
            "Export"
        )


        cancel_button = QPushButton(
            "Cancel"
        )


        export_button.clicked.connect(
            self.accept_export
        )


        cancel_button.clicked.connect(
            self.reject
        )


        button_row.addWidget(
            export_button
        )


        button_row.addWidget(
            cancel_button
        )


        layout.addLayout(
            button_row
        )



    # --------------------------------------------------
    # Folder
    # --------------------------------------------------

    def choose_folder(
        self
    ):


        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Export Folder"
        )


        if folder:

            self.output_folder = folder


            self.folder_label.setText(
                folder
            )



    # --------------------------------------------------
    # Accept
    # --------------------------------------------------

    def accept_export(
        self
    ):

        self.settings.set_range(
            self.start_frame.value(),
            self.end_frame.value()
        )


        self.settings.output_folder = (
            self.output_folder
        )


        super().accept()



    # --------------------------------------------------
    # Values
    # --------------------------------------------------

    def get_settings(
        self
    ):

        return {

            "start":
                self.start_frame.value(),

            "end":
                self.end_frame.value(),

            "folder":
                self.output_folder

        }