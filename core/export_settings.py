# core/export_settings.py


class ExportSettings:


    def __init__(self):

        self.start_frame = 0

        self.end_frame = 0


        self.output_folder = ""


        self.frame_prefix = "frame"



    # --------------------------------------------------
    # Set range
    # --------------------------------------------------

    def set_range(
        self,
        start,
        end
    ):

        self.start_frame = max(
            0,
            start
        )


        self.end_frame = max(
            self.start_frame,
            end
        )



    # --------------------------------------------------
    # Get range
    # --------------------------------------------------

    def get_range(self):

        return (
            self.start_frame,
            self.end_frame
        )



    # --------------------------------------------------
    # Frame filename
    # --------------------------------------------------

    def filename(
        self,
        number
    ):

        return (
            f"{self.frame_prefix}_"
            f"{number:04d}.dds"
        )