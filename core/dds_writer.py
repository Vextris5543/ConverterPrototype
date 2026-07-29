# core/dds_writer.py

import os
import subprocess
import tempfile
import shutil



class DDSWriter:
    """
    Handles converting PNG/RGBA images into uncompressed DDS files.

    Uses:
        texconv.exe

    Output:
        B8G8R8A8_UNORM DDS

    Settings:
        - No compression
        - No mipmaps
        - Full alpha support
    """



    def __init__(
        self,
        texconv_path="texconv.exe"
    ):

        self.texconv_path = texconv_path



    # --------------------------------------------------
    # Write single DDS
    # --------------------------------------------------

    def write(
        self,
        image,
        filename
    ):

        if image is None:

            return False



        folder = os.path.dirname(
            filename
        )


        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )



        temp_dir = tempfile.mkdtemp()



        try:

            tga_path = os.path.join(
                temp_dir,
                "input.tga"
            )


            # Ensure RGBA before export

            image = image.convert(
                "RGBA"
            )


            image.save(
                tga_path,
                "TGA"
            )

            result = subprocess.run(
                [
                    self.texconv_path,

                    # Uncompressed 32-bit RGBA
                    "-f",
                    "B8G8R8A8_UNORM",

                    # No mipmaps
                    "-m",
                    "1",

                    # Overwrite existing files
                    "-y",

                    "-o",
                    temp_dir,

                    tga_path
                ],

                stdout=subprocess.PIPE,

                stderr=subprocess.PIPE,

                text=True
            )



            if result.returncode != 0:

                print(
                    "texconv failed:"
                )

                print(
                    result.stdout
                )

                print(
                    result.stderr
                )

                return False



            converted = os.path.join(
                temp_dir,
                "input.dds"
            )



            if not os.path.exists(
                converted
            ):

                return False



            shutil.move(
                converted,
                filename
            )



            return True



        finally:

            shutil.rmtree(
                temp_dir,
                ignore_errors=True
            )



    # --------------------------------------------------
    # Write sequence
    # --------------------------------------------------

    def write_sequence(
        self,
        images,
        folder
    ):


        os.makedirs(
            folder,
            exist_ok=True
        )



        for index, image in enumerate(
            images
        ):


            filename = os.path.join(
                folder,
                f"frame_{index:04d}.dds"
            )



            if not self.write(
                image,
                filename
            ):

                return False



        return True