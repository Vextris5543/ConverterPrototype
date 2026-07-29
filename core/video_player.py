# core/video_player.py

import cv2


class VideoPlayer:
    """
    Handles video loading and frame retrieval.
    """

    def __init__(self):

        self.capture = None

        self.path = None

        self.fps = 30

        self.frame_count = 0

        self.width = 0

        self.height = 0

        self.current_frame = 0


    # --------------------------------------------------
    # Load
    # --------------------------------------------------

    def load(
        self,
        path
    ):

        self.close()


        self.capture = cv2.VideoCapture(
            path
        )


        if not self.capture.isOpened():

            self.capture = None

            return False


        self.path = path


        self.fps = self.capture.get(
            cv2.CAP_PROP_FPS
        )


        if self.fps <= 0:

            self.fps = 30


        self.frame_count = int(
            self.capture.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )


        self.width = int(
            self.capture.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )


        self.height = int(
            self.capture.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )


        self.current_frame = 0


        return True


    # --------------------------------------------------
    # Read Current Frame
    # --------------------------------------------------

    def get_frame(
        self
    ):

        if self.capture is None:

            return None


        success, frame = (
            self.capture.read()
        )


        if not success:

            return None


        self.current_frame += 1


        return frame


    # --------------------------------------------------
    # Seek
    # --------------------------------------------------

    def seek(
        self,
        frame_number
    ):

        if self.capture is None:

            return None


        frame_number = max(
            0,
            min(
                frame_number,
                self.frame_count - 1
            )
        )


        self.capture.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number
        )


        self.current_frame = frame_number


        return self.get_frame()


    # --------------------------------------------------
    # First Frame
    # --------------------------------------------------

    def first_frame(
        self
    ):

        return self.seek(
            0
        )


    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    def close(
        self
    ):

        if self.capture:

            self.capture.release()

            self.capture = None


    def __del__(
        self
    ):

        self.close()