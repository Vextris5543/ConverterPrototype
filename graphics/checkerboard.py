# graphics/checkerboard.py

from PySide6.QtGui import QColor


class Checkerboard:
    """
    Draws the transparent background grid.
    """

    def __init__(self):

        self.tile_size = 20

        self.light = QColor(
            65,
            65,
            65
        )

        self.dark = QColor(
            45,
            45,
            45
        )

    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

    def draw(
        self,
        painter,
        rect
    ):

        tile = self.tile_size

        width = rect.width()
        height = rect.height()

        for y in range(
            0,
            int(height),
            tile
        ):

            for x in range(
                0,
                int(width),
                tile
            ):

                if (
                    (x // tile)
                    +
                    (y // tile)
                ) % 2 == 0:

                    painter.fillRect(
                        x,
                        y,
                        tile,
                        tile,
                        self.light
                    )

                else:

                    painter.fillRect(
                        x,
                        y,
                        tile,
                        tile,
                        self.dark
                    )