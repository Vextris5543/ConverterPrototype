import numpy as np


class TextureMask:

    def __init__(
        self,
        rgba
    ):

        self.rgba = rgba


        # Preview position
        self.capture_x = 0
        self.capture_y = 0


        # Scale
        self.scale = 1.0
        # Rotation (degrees)
        self.rotation = 0.0

        # Frame inside template
        self.frame_x = 0
        self.frame_y = 0
        self.capture_width = rgba.shape[1]
        self.capture_height = rgba.shape[0]


        self.find_blue_frame()



    def find_blue_frame(
        self
    ):

        rgb = self.rgba[:, :, :3]


        blue_pixels = (
            (rgb[:, :, 0] == 0)
            &
            (rgb[:, :, 1] == 0)
            &
            (rgb[:, :, 2] == 255)
        )


        ys, xs = np.where(
            blue_pixels
        )


        if len(xs) == 0:

            return


        # store frame location separately
        self.frame_x = int(xs.min())
        self.frame_y = int(ys.min())


        self.capture_width = int(
            xs.max() - xs.min() + 1
        )


        self.capture_height = int(
            ys.max() - ys.min() + 1
        )



    def get_rect(
        self
    ):

        return (
            self.frame_x,
            self.frame_y,
            self.capture_width,
            self.capture_height
        )



    def resize(
        self,
        width,
        height
    ):

        self.capture_width = max(
            1,
            int(width)
        )

        self.capture_height = max(
            1,
            int(height)
        )