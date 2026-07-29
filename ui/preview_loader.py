# ui/preview_loader.py

from PySide6.QtGui import QImage, QPixmap

from core.dds_loader import DDSLoader



class PreviewLoader:

    def __init__(
        self,
        project,
        scene
    ):

        self.project = project
        self.scene = scene

        self.dds_loader = DDSLoader()



    def set_frame(
        self,
        frame
    ):

        if frame is None:

            return


        height, width = frame.shape[:2]


        # OpenCV frames are BGR
        # Convert to RGB for Qt

        if frame.shape[2] == 3:

            rgb = frame[:, :, ::-1].copy()


            image = QImage(
                rgb.data,
                width,
                height,
                width * 3,
                QImage.Format_RGB888
            )


        elif frame.shape[2] == 4:

            rgba = frame[:, :, [2, 1, 0, 3]].copy()


            image = QImage(
                rgba.data,
                width,
                height,
                width * 4,
                QImage.Format_RGBA8888
            )


        else:

            return



        pixmap = QPixmap.fromImage(
            image.copy()
        )


        self.scene.set_video(
            pixmap
        )



    def set_dds(
        self,
        path
    ):

        mask = self.dds_loader.load(
            path
        )


        if mask is None:

            return False



        # Store template object
        # No transparency modification.
        # No black removal.
        # The template itself controls visibility.

        self.project.mask = mask


        rgba = mask.rgba.copy()


        image = QImage(
            rgba.data,
            rgba.shape[1],
            rgba.shape[0],
            rgba.shape[1] * 4,
            QImage.Format_RGBA8888
        )


        pixmap = QPixmap.fromImage(
            image.copy()
        )


        self.scene.set_dds(
            pixmap
        )


        return True