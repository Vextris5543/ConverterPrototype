# interaction/timeline_controller.py

from PySide6.QtCore import (
    QObject,
    Signal,
    QTimer,
)


class TimelineController(QObject):
    """
    Controls video playback and timeline movement.
    """

    frameChanged = Signal(int)

    def __init__(self, project):

        super().__init__()

        self.project = project

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.next_frame
        )

    # --------------------------------------------------
    # Playback
    # --------------------------------------------------

    def play(self):

        if self.project.video_player is None:
            return

        fps = self.project.video_player.fps

        if fps <= 0:
            fps = 30

        interval = int(
            1000 / fps
        )

        self.timer.start(
            interval
        )

        self.project.playing = True

    def pause(self):

        self.timer.stop()

        self.project.playing = False

    # --------------------------------------------------
    # Frames
    # --------------------------------------------------

    def next_frame(self):

        player = self.project.video_player

        if player is None:
            return

        next_index = (
            self.project.current_frame + 1
        )

        if next_index >= player.frame_count:

            self.pause()

            return

        self.project.current_frame = (
            next_index
        )

        self.frameChanged.emit(
            next_index
        )

    def seek(self, frame):

        player = self.project.video_player

        if player is None:
            return

        frame = max(
            0,
            min(
                frame,
                player.frame_count - 1
            )
        )

        self.project.current_frame = frame

        self.frameChanged.emit(
            frame
        )

    # --------------------------------------------------
    # Range
    # --------------------------------------------------

    def set_range(
        self,
        start,
        end
    ):

        self.project.export_start = start

        self.project.export_end = end

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self):

        self.pause()

        self.project.current_frame = 0

        self.frameChanged.emit(
            0
        )