# core/frame_processor.py

import cv2
import numpy as np


class FrameProcessor:
    """
    Handles cropping and resizing frames for DDS export.
    """

    def __init__(self, project):

        self.project = project

    # --------------------------------------------------
    # Crop Capture Area
    # --------------------------------------------------

    def crop_capture(self, frame):

        if frame is None:
            return None

        mask = self.project.mask

        x = int(mask.capture_x)
        y = int(mask.capture_y)

        w = int(mask.capture_width)
        h = int(mask.capture_height)

        frame_h, frame_w = frame.shape[:2]

        # Clamp rectangle to frame

        x = max(0, min(x, frame_w))
        y = max(0, min(y, frame_h))

        w = max(1, min(w, frame_w - x))
        h = max(1, min(h, frame_h - y))

        return frame[y:y + h, x:x + w].copy()

    # --------------------------------------------------
    # Resize To Guide Size
    # --------------------------------------------------

    def resize_to_guide(self, image):

        if image is None:
            return None

        mask = self.project.mask

        return cv2.resize(
            image,
            (
                int(mask.guide_width),
                int(mask.guide_height)
            ),
            interpolation=cv2.INTER_LINEAR
        )

    # --------------------------------------------------
    # Full Processing
    # --------------------------------------------------

    def process(self, frame):

        cropped = self.crop_capture(frame)

        if cropped is None:
            return None

        return self.resize_to_guide(cropped)

    # --------------------------------------------------
    # Create Transparent DDS Canvas
    # --------------------------------------------------

    def create_canvas(self):

        mask = self.project.mask

        return np.zeros(
            (
                int(mask.dds_height),
                int(mask.dds_width),
                4
            ),
            dtype=np.uint8
        )

    # --------------------------------------------------
    # Paste Into DDS Canvas
    # --------------------------------------------------

    def paste_into_canvas(self, canvas, image):

        if canvas is None or image is None:
            return canvas

        mask = self.project.mask

        x = int(mask.guide_x)
        y = int(mask.guide_y)

        h, w = image.shape[:2]

        canvas[
            y:y + h,
            x:x + w
        ] = image

        return canvas

    # --------------------------------------------------
    # Complete Export Frame
    # --------------------------------------------------

    def build_export_frame(self, frame):

        processed = self.process(frame)

        if processed is None:
            return None

        canvas = self.create_canvas()

        return self.paste_into_canvas(
            canvas,
            processed
        )