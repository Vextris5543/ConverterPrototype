# ui/drag_drop_handler.py

import os


class DragDropHandler:
    """
    Handles drag and drop file detection.

    Determines whether dropped files are:
        - Video files
        - DDS templates
    """

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".webm",
        ".wmv",
    }

    DDS_EXTENSIONS = {
        ".dds",
    }

    def __init__(
        self,
        video_callback,
        dds_callback
    ):

        self.video_callback = (
            video_callback
        )

        self.dds_callback = (
            dds_callback
        )

    # --------------------------------------------------
    # Drop
    # --------------------------------------------------

    def handle_files(
        self,
        files
    ):

        for file in files:

            ext = os.path.splitext(
                file
            )[1].lower()


            if ext in self.VIDEO_EXTENSIONS:

                self.video_callback(
                    file
                )


            elif ext in self.DDS_EXTENSIONS:

                self.dds_callback(
                    file
                )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def is_video(
        self,
        filename
    ):

        return (
            os.path.splitext(filename)[1]
            .lower()
            in self.VIDEO_EXTENSIONS
        )


    def is_dds(
        self,
        filename
    ):

        return (
            os.path.splitext(filename)[1]
            .lower()
            in self.DDS_EXTENSIONS
        )


    def filter_files(
        self,
        files
    ):

        videos = []
        dds = []


        for file in files:

            if self.is_video(file):

                videos.append(file)

            elif self.is_dds(file):

                dds.append(file)


        return (
            videos,
            dds
        )