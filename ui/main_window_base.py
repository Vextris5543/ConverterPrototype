# ui/main_window_base.py

from PySide6.QtWidgets import QFileDialog


class MainWindowBase:
    """
    MainWindow implementation methods.

    Loaded into MainWindow to keep the UI file small.
    """

    # --------------------------------------------------
    # Video Loading
    # --------------------------------------------------

    def load_video(self, path):

        if not self.player.load(path):
            return

        self.project.video_path = path

        self.asset_panel.set_video(
            path
        )

        self.timeline.set_frame_count(
            self.player.frame_count
        )

        frame = self.player.get_frame(0)

        if frame is not None:

            self.project.current_frame = 0

            self.preview.set_frame(
                frame
            )

        self.update_transform_panel()

    # --------------------------------------------------
    # DDS Loading
    # --------------------------------------------------

    def load_dds(self, path):

        if self.preview.loader.set_dds(path):

            self.project.dds_path = path

            self.asset_panel.set_dds(
                path
            )

            self.update_transform_panel()

            self.preview.update()

    # --------------------------------------------------
    # Dialogs
    # --------------------------------------------------

    def open_video_dialog(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            (
                "Video Files "
                "(*.mp4 *.avi *.mov *.mkv *.webm)"
            )
        )

        if path:

            self.load_video(path)

    def open_dds_dialog(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open DDS Template",
            "",
            "DDS Files (*.dds)"
        )

        if path:

            self.load_dds(path)

    # --------------------------------------------------
    # Playback
    # --------------------------------------------------

    def play_video(self):

        self.project.playing = True

        self.timeline_controller.play()

    def pause_video(self):

        self.project.playing = False

        self.timeline_controller.pause()

    def seek_video(self, frame):

        image = self.player.get_frame(
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
            self.player.frame_count
        )

    # --------------------------------------------------
    # Transform
    # --------------------------------------------------

    def set_capture_x(self, value):

        if not self.project.has_dds:
            return

        self.project.mask.capture_x = value

        self.preview.update()

    def set_capture_y(self, value):

        if not self.project.has_dds:
            return

        self.project.mask.capture_y = value

        self.preview.update()

    def set_capture_scale(self, value):

        if not self.project.has_dds:
            return

        self.transform_controller.set_scale(
            value
        )

        self.preview.update()

    def set_capture_rotation(self, value):

        if not self.project.has_dds:
            return

        self.transform_controller.set_rotation(
            value
        )

        self.preview.update()

    def set_overlay_opacity(self, value):

        self.project.overlay_opacity = value

        self.preview.update()

    def reset_transform(self):

        if not self.project.has_dds:
            return

        self.transform_controller.reset()

        self.update_transform_panel()

        self.preview.update()

    def update_transform_panel(self):

        if not self.project.has_dds:
            return

        mask = self.project.mask

        self.transform_panel.set_values(
            mask.capture_x,
            mask.capture_y,
            mask.scale,
            mask.rotation,
            self.project.overlay_opacity
        )

    # --------------------------------------------------
    # View
    # --------------------------------------------------

    def reset_view(self):

        self.zoom_controller.reset_view()

        self.preview.update()

    # --------------------------------------------------
    # Project
    # --------------------------------------------------

    def save_project(self):

        pass

    def load_project(self):

        pass

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    def export_sequence(self):

        pass