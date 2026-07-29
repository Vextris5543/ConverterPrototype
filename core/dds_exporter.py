# core/dds_exporter.py

import os

import cv2
import numpy as np

from PIL import Image

from core.dds_writer import DDSWriter


class DDSExporter:
    """
    Exports video frames using the blue DDS template frame.
    """

    def __init__(
        self,
        texconv_path="texconv.exe"
    ):

        self.template = None

        self.writer = DDSWriter(
            texconv_path
        )

    # --------------------------------------------------
    # Template
    # --------------------------------------------------

    def set_template(
        self,
        mask
    ):

        self.template = mask

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    def export_frames(
        self,
        frames,
        output_folder
    ):

        if self.template is None:

            return False

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        images = []

        for frame in frames:

            images.append(
                self.create_dds_frame(
                    frame
                )
            )

        return self.writer.write_sequence(
            images,
            output_folder
        )

    # --------------------------------------------------
    # Create DDS image
    # --------------------------------------------------

    def create_dds_frame(
        self,
        frame
    ):

        template = self.template.rgba

        rgb = template[:, :, :3]

        # Find pure blue pixels
        blue = (
            (rgb[:, :, 0] == 0)
            &
            (rgb[:, :, 1] == 0)
            &
            (rgb[:, :, 2] == 255)
        )

        ys, xs = np.where(
            blue
        )

        if len(xs) == 0:

            return Image.fromarray(
                template.copy(),
                "RGBA"
            )

        # ------------------------------------------
        # Polygon
        # ------------------------------------------

        points = np.column_stack(
            (
                xs,
                ys
            )
        ).astype(
            np.int32
        )

        hull = cv2.convexHull(
            points
        )

        polygon_mask = np.zeros(
            (
                template.shape[0],
                template.shape[1]
            ),
            dtype=np.uint8
        )

        cv2.fillPoly(
            polygon_mask,
            [hull],
            255
        )

        # ------------------------------------------
        # Bounding rectangle
        # ------------------------------------------

        x1 = xs.min()
        y1 = ys.min()

        x2 = xs.max()
        y2 = ys.max()

        width = x2 - x1 + 1
        height = y2 - y1 + 1

        # ------------------------------------------
        # Convert OpenCV frame
        # ------------------------------------------

        if frame.shape[2] == 3:

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGBA
            )

        elif frame.shape[2] == 4:

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGRA2RGBA
            )


        video = Image.fromarray(
            frame
        )
        
     
        video = video.resize(
            (
                width,
                height
            ),
            Image.Resampling.LANCZOS
        )
        
        
        video_pixels = np.array(
            video
        )

        # ------------------------------------------
        # Start from template
        # ------------------------------------------

        output = template.copy()

        # Replace rectangle with resized video
        output[
            y1:y2 + 1,
            x1:x2 + 1
        ] = video_pixels

        # Remove anything outside the polygon
        inside = polygon_mask == 255

        output[~inside] = (
            0,
            0,
            0,
            0
        )

        # IMPORTANT:
        # Do NOT resize again.
        # The template is already 256x250.

        return Image.fromarray(
            output,
            "RGBA"
        )