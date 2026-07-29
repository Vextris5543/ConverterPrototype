# core/image_converter.py

import numpy as np

from PySide6.QtGui import (
    QImage,
    QPixmap,
)


class ImageConverter:
    """
    Shared image conversion utilities.

    Converts between:
        - OpenCV frames
        - NumPy RGBA arrays
        - Qt images
        - Qt pixmaps
    """

    # --------------------------------------------------
    # OpenCV BGR
    # --------------------------------------------------

    @staticmethod
    def cv_to_pixmap(
        frame
    ):

        if frame is None:
            return None


        import cv2


        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        return ImageConverter.rgb_to_pixmap(
            rgb
        )

    # --------------------------------------------------
    # RGB Array
    # --------------------------------------------------

    @staticmethod
    def rgb_to_pixmap(
        rgb
    ):

        rgb = np.ascontiguousarray(
            rgb
        )


        height, width, channels = (
            rgb.shape
        )


        bytes_per_line = (
            width * channels
        )


        image = QImage(
            rgb.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888
        )


        return QPixmap.fromImage(
            image.copy()
        )

    # --------------------------------------------------
    # RGBA Array
    # --------------------------------------------------

    @staticmethod
    def rgba_to_pixmap(
        rgba
    ):

        rgba = np.ascontiguousarray(
            rgba
        )


        height, width, channels = (
            rgba.shape
        )


        bytes_per_line = (
            width * channels
        )


        image = QImage(
            rgba.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGBA8888
        )


        return QPixmap.fromImage(
            image.copy()
        )

    # --------------------------------------------------
    # QImage
    # --------------------------------------------------

    @staticmethod
    def qimage_to_pixmap(
        image
    ):

        return QPixmap.fromImage(
            image.copy()
        )

    # --------------------------------------------------
    # Pixmap
    # --------------------------------------------------

    @staticmethod
    def pixmap_to_rgba(
        pixmap
    ):

        image = pixmap.toImage()

        image = image.convertToFormat(
            QImage.Format_RGBA8888
        )


        width = image.width()

        height = image.height()


        ptr = image.bits()

        ptr.setsize(
            image.sizeInBytes()
        )


        array = np.frombuffer(
            ptr,
            np.uint8
        )


        return array.reshape(
            (
                height,
                width,
                4
            )
        )