# graphics/qt_image.py

import numpy as np

from PySide6.QtGui import (
    QImage,
    QPixmap
)


class QtImage:
    """
    Image conversion helpers.

    OpenCV:
        BGR  -> QPixmap

    OpenCV:
        BGRA -> QPixmap

    Pillow:
        Image -> QPixmap

    NumPy:
        RGB -> QPixmap
    """

    # --------------------------------------------------
    # OpenCV BGR -> QPixmap
    # --------------------------------------------------

    @staticmethod
    def from_bgr(frame):

        if frame is None:
            return None

        rgb = frame[:, :, ::-1].copy()

        h, w, ch = rgb.shape

        image = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        return QPixmap.fromImage(image.copy())

    # --------------------------------------------------
    # OpenCV BGRA -> QPixmap
    # --------------------------------------------------

    @staticmethod
    def from_bgra(frame):

        if frame is None:
            return None

        rgba = frame.copy()

        h, w, ch = rgba.shape

        image = QImage(
            rgba.data,
            w,
            h,
            ch * w,
            QImage.Format_RGBA8888
        )

        return QPixmap.fromImage(image.copy())

    # --------------------------------------------------
    # RGB NumPy -> QPixmap
    # --------------------------------------------------

    @staticmethod
    def from_rgb(frame):

        if frame is None:
            return None

        rgb = np.ascontiguousarray(frame)

        h, w, ch = rgb.shape

        image = QImage(
            rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        return QPixmap.fromImage(image.copy())

    # --------------------------------------------------
    # RGBA NumPy -> QPixmap
    # --------------------------------------------------

    @staticmethod
    def from_rgba(frame):

        if frame is None:
            return None

        rgba = np.ascontiguousarray(frame)

        h, w, ch = rgba.shape

        image = QImage(
            rgba.data,
            w,
            h,
            ch * w,
            QImage.Format_RGBA8888
        )

        return QPixmap.fromImage(image.copy())

    # --------------------------------------------------
    # Pillow -> QPixmap
    # --------------------------------------------------

    @staticmethod
    def from_pillow(image):

        if image is None:
            return None

        image = image.convert("RGBA")

        data = image.tobytes()

        qimage = QImage(
            data,
            image.width,
            image.height,
            image.width * 4,
            QImage.Format_RGBA8888
        )

        return QPixmap.fromImage(qimage.copy())

    # --------------------------------------------------
    # Scale
    # --------------------------------------------------

    @staticmethod
    def scaled(
        pixmap,
        width,
        height,
        keep_aspect=True
    ):

        if pixmap is None:
            return None

        from PySide6.QtCore import Qt

        mode = (
            Qt.KeepAspectRatio
            if keep_aspect
            else Qt.IgnoreAspectRatio
        )

        return pixmap.scaled(
            width,
            height,
            mode,
            Qt.SmoothTransformation
        )