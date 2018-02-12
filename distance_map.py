from __future__ import print_function
import os
import click
import glob
import subprocess
from PIL import Image

@click.command()
@click.argument("input_folder",
                type=click.Path(
                    exists=True,
                    file_okay=False)
               )
@click.argument("output_filename",
                type=click.Path())
def main(input_folder, output_filename):
    """segment all the files in the folder"""
    input_filenames = sorted(glob.glob(os.path.join(input_folder, "*.tif")))
    d = len(input_filenames)
    first_filename = input_filenames[0]
    first_image = Image.open(first_filename)
    w, h = first_image.size
    print(output_filename)
    dims_output_filename = output_filename.replace(".raw", ".txt")
    print(w, h, d, dims_output_filename)
    with open(dims_output_filename, "w") as dims_output:
        print(w, h, d, file=dims_output)
    command = "fiji --system --ij2 --headless --run distance_map_macro.py 'input_file=\"{}\",output_file=\"{}\"'".format(
        input_filenames[0],
        output_filename
    )
    print(command)
    subprocess.check_call(command, shell=True)


if __name__ == "__main__":
    main()
