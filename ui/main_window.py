# ui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QDialog,
)

from PySide6.QtCore import QTimer


from ui.preview_widget import PreviewWidget
from ui.timeline_widget import TimelineWidget
from ui.asset_panel import AssetPanel
from ui.transform_panel import TransformPanel
from ui.menu_bar import MenuBar
from ui.export_dialog import ExportDialog


from core.video_player import VideoPlayer
from core.project_state import ProjectState
from core.dds_exporter import DDSExporter



class MainWindow(QMainWindow):

    """
    Main application window.

    Connects:
        - Preview
        - Timeline
        - Assets
        - Transform controls
        - Menus
        - Export
    """



    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "DDS Animation Creator"
        )


        self.resize(
            1400,
            900
        )



        # --------------------------------------------------
        # State
        # --------------------------------------------------

        self.project = ProjectState()


        self.video_player = VideoPlayer()


        self.project.video_player = (
            self.video_player
        )


        self.exporter = DDSExporter()



        # --------------------------------------------------
        # Playback Timer
        # --------------------------------------------------

        self.play_timer = QTimer(
            self
        )


        self.play_timer.timeout.connect(
            self.next_frame
        )



        # --------------------------------------------------
        # UI
        # --------------------------------------------------

        self.build_ui()

        self.connect_signals()



    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def build_ui(self):

        self.menu = MenuBar(
            self
        )


        self.setMenuBar(
            self.menu
        )



        self.preview = PreviewWidget(
            self.project,
            self
        )


        self.timeline = TimelineWidget(
            self
        )


        self.assets = AssetPanel(
            self
        )


        self.transform = TransformPanel(
            self
        )



        central = QWidget()


        layout = QVBoxLayout(
            central
        )


        layout.addWidget(
            self.preview,
            1
        )


        layout.addWidget(
            self.timeline
        )


        self.setCentralWidget(
            central
        )



    # --------------------------------------------------
    # Signals
    # --------------------------------------------------

    def connect_signals(self):


        self.menu.openVideo.connect(
            self.open_video
        )


        self.menu.openDDS.connect(
            self.open_dds
        )


        self.menu.exportDDS.connect(
            self.export_dds
        )


        self.menu.resetView.connect(
            self.reset_view
        )


        self.menu.resetTransform.connect(
            self.reset_transform
        )



        self.preview.videoDropped.connect(
            self.load_video
        )


        self.preview.ddsDropped.connect(
            self.load_dds
        )



        self.timeline.seekRequested.connect(
            self.seek_video
        )


        self.timeline.playClicked.connect(
            self.play_video
        )


        self.timeline.pauseClicked.connect(
            self.pause_video
        )



        self.transform.scaleChanged.connect(
            self.update_scale
        )


        self.transform.opacityChanged.connect(
            self.update_opacity
        )



    # --------------------------------------------------
    # Video
    # --------------------------------------------------

    def open_video(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video"
        )


        if path:

            self.load_video(
                path
            )



    def load_video(
        self,
        path
    ):


        if not self.video_player.load(
            path
        ):

            return



        self.project.set_video(
            path,
            self.video_player
        )



        self.timeline.set_frame_count(
            self.video_player.frame_count
        )



        frame = self.video_player.first_frame()



        if frame is not None:

            self.preview.set_frame(
                frame
            )



        self.assets.set_video(
            path
        )



    # --------------------------------------------------
    # Playback
    # --------------------------------------------------

    def play_video(self):

        if self.video_player.capture is None:

            return



        interval = int(
            1000 /
            self.video_player.fps
        )


        self.play_timer.start(
            interval
        )



    def pause_video(self):

        self.play_timer.stop()



    def next_frame(self):

        frame = self.video_player.get_frame()



        if frame is None:

            self.pause_video()

            return



        current = (
            self.video_player.current_frame
        )



        self.project.current_frame = current



        self.preview.set_frame(
            frame
        )



        self.timeline.update_frame(
            current,
            self.video_player.frame_count
        )



    # --------------------------------------------------
    # DDS
    # --------------------------------------------------

    def open_dds(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open DDS Template",
            filter="DDS Files (*.dds)"
        )


        if path:

            self.load_dds(
                path
            )



    def load_dds(
        self,
        path
    ):


        if self.preview.set_dds(
            path
        ):


            self.exporter.set_template(
                self.project.mask
            )


            self.assets.set_dds(
                path
            )



    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    def export_dds(self):

        if self.project.mask is None:

            return



        if self.video_player.capture is None:

            return



        dialog = ExportDialog(
            self.video_player.frame_count,
            self
        )



        if dialog.exec() != QDialog.Accepted:

            return



        settings = dialog.settings



        start_frame = (
            settings.start_frame
        )


        end_frame = (
            settings.end_frame
        )



        print(
            "Export:",
            start_frame,
            end_frame
        )



        frames = []



        for frame_number in range(
            start_frame,
            end_frame + 1
        ):


            frame = self.video_player.seek(
                frame_number
            )


            if frame is not None:

                frames.append(
                    frame
                )



        print(
            "Frames collected:",
            len(frames)
        )



        if len(frames) == 0:

            print(
                "No frames collected"
            )

            return



        self.exporter.set_template(
            self.project.mask
        )



        result = self.exporter.export_frames(
            frames,
            settings.output_folder
        )



        print(
            "Export result:",
            result
        )



    # --------------------------------------------------
    # Timeline
    # --------------------------------------------------

    def seek_video(
        self,
        frame
    ):


        image = self.video_player.seek(
            frame
        )



        if image is None:

            return



        self.project.current_frame = frame



        self.preview.set_frame(
            image
        )



        self.timeline.update_frame(
            frame,
            self.video_player.frame_count
        )



    # --------------------------------------------------
    # Transform
    # --------------------------------------------------

    def update_scale(
        self,
        value
    ):


        if self.project.mask:

            self.project.mask.scale = (
                value / 100
            )



        self.preview.update()



    def update_opacity(
        self,
        value
    ):


        self.project.overlay_opacity = (
            value / 100
        )


        self.preview.update()



    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset_view(self):

        self.project.reset_view()

        self.preview.update()



    def reset_transform(self):

        self.project.reset_transform()

        self.preview.update()