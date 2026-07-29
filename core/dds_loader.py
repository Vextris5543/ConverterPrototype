# core/dds_loader.py

import numpy as np

from PIL import Image

from core.texture_mask import TextureMask



class DDSLoader:

    def __init__(
        self
    ):

        self.last_mask = None



    def load(
        self,
        path
    ):

        image = Image.open(
            path
        )


        image = image.convert(
            "RGBA"
        )


        rgba = np.array(
            image
        )


        mask = TextureMask(
            rgba
        )


        self.last_mask = mask


        return mask