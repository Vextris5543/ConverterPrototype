# core/project_state.py

from PySide6.QtCore import QObject, Signal


class ProjectState(QObject):
    """
    Stores current project data.

    Contains:
        - Video state
        - DDS template state
        - Transform values
        - Preview settings
    """

    changed = Signal()

    # --------------------------------------------------
    # Init
    # --------------------------------------------------

    def __init__(self):

        super().__init__()


        # Assets

        self.video_path = None

        self.dds_path = None


        self.video_player = None


        # DDS

        self.mask = None

        self.has_dds = False


        # Playback

        self.playing = False

        self.current_frame = 0

        self.total_frames = 0


        # Transform

        self.zoom = 1.0

        self.pan_x = 0

        self.pan_y = 0


        self.overlay_opacity = 0.5


        # Preview

        self.show_checkerboard = True

        self.show_capture = True

        self.show_guides = True


    # --------------------------------------------------
    # Video
    # --------------------------------------------------

    def set_video(
        self,
        path,
        player=None
    ):

        self.video_path = path

        self.video_player = player

        self.emit_changed()


    def clear_video(self):

        self.video_path = None

        self.video_player = None

        self.current_frame = 0

        self.total_frames = 0

        self.emit_changed()


    # --------------------------------------------------
    # DDS
    # --------------------------------------------------

    def set_dds(
        self,
        path,
        mask
    ):

        self.dds_path = path

        self.mask = mask

        self.has_dds = True

        self.emit_changed()


    def clear_dds(self):

        self.dds_path = None

        self.mask = None

        self.has_dds = False

        self.emit_changed()


    # --------------------------------------------------
    # Transform
    # --------------------------------------------------

    def reset_transform(self):

        if self.mask:

            self.mask.capture_x = 0

            self.mask.capture_y = 0

            self.mask.scale = 1.0

            self.mask.rotation = 0


        self.overlay_opacity = 0.5

        self.emit_changed()


    def set_scale(
        self,
        value
    ):

        if self.mask:

            self.mask.scale = value


        self.emit_changed()


    def set_position(
        self,
        x,
        y
    ):

        if self.mask:

            self.mask.capture_x = x

            self.mask.capture_y = y


        self.emit_changed()


    # --------------------------------------------------
    # Preview
    # --------------------------------------------------

    def reset_view(self):

        self.zoom = 1.0

        self.pan_x = 0

        self.pan_y = 0

        self.emit_changed()


    # --------------------------------------------------
    # Signal
    # --------------------------------------------------

    def emit_changed(self):

        self.changed.emit()