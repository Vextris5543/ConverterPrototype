# core/dds_loader.py

from PIL import Image
import struct


class DDSLoader:
    """
    Loads DDS texture templates.

    Prototype goals:
    - Read DDS dimensions
    - Read alpha information
    - Convert to RGBA
    - Find visible texture area
    """


    def __init__(self):

        self.path = None

        self.width = 0
        self.height = 0

        self.image = None

        self.alpha_bbox = None

        self.format = None


    # --------------------------------------------------
    # Load DDS
    # --------------------------------------------------

    def load(self, filename):

        self.path = filename


        try:

            img = Image.open(filename)

            self.image = img.convert("RGBA")

            self.width, self.height = self.image.size


            self.format = img.info.get(
                "compression",
                "unknown"
            )


            self.alpha_bbox = self.find_alpha_bounds()


            return True


        except Exception as e:

            print(
                "DDS Load Error:",
                e
            )

            return False



    # --------------------------------------------------
    # Find non transparent area
    # --------------------------------------------------

    def find_alpha_bounds(self):

        if self.image is None:
            return None


        alpha = self.image.getchannel("A")


        bbox = alpha.getbbox()


        if bbox is None:

            # Entire texture transparent

            return (
                0,
                0,
                self.width,
                self.height
            )


        return bbox



    # --------------------------------------------------
    # Get preview image
    # --------------------------------------------------

    def get_image(self):

        return self.image



    # --------------------------------------------------
    # Get visible mask area
    # --------------------------------------------------

    def get_visible_rect(self):

        return self.alpha_bbox



    # --------------------------------------------------
    # DDS information
    # --------------------------------------------------

    def info(self):

        return {

            "width":
                self.width,

            "height":
                self.height,

            "format":
                self.format,

            "visible_area":
                self.alpha_bbox

        }