# core/video_capture.py

import cv2


class VideoCaptureReader:
    """
    Lightweight video frame reader.

    Used by:
        - Exporter
        - Batch frame processing
        - Preview tools
    """

    def __init__(self):

        self.cap = None

        self.path = None

        self.fps = 30

        self.frame_count = 0


    # --------------------------------------------------
    # Open
    # --------------------------------------------------

    def open(
        self,
        path
    ):

        self.cap = cv2.VideoCapture(
            path
        )

        if not self.cap.isOpened():

            self.cap = None

            return False


        self.path = path


        self.fps = (
            self.cap.get(
                cv2.CAP_PROP_FPS
            )
        )


        if self.fps <= 0:

            self.fps = 30


        self.frame_count = int(
            self.cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )


        return True


    # --------------------------------------------------
    # Read
    # --------------------------------------------------

    def read(
        self,
        frame_number=None
    ):

        if self.cap is None:

            return None


        if frame_number is not None:

            self.cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                frame_number
            )


        success, frame = (
            self.cap.read()
        )


        if not success:

            return None


        return frame


    # --------------------------------------------------
    # Range
    # --------------------------------------------------

    def read_range(
        self,
        start,
        end
    ):

        frames = []


        for index in range(
            start,
            end + 1
        ):

            frame = self.read(
                index
            )


            if frame is None:

                break


            frames.append(
                frame
            )


        return frames


    # --------------------------------------------------
    # Close
    # --------------------------------------------------

    def close(self):

        if self.cap:

            self.cap.release()

            self.cap = None


    def __del__(self):

        self.close()