import os
import click
import glob
import subprocess
from tqdm import tqdm

@click.command()
@click.argument("input_folder",
                type=click.Path(
                    exists=True,
                    file_okay=False)
               )
@click.argument("output_folder",
                type=click.Path(
                    exists=True,
                    file_okay=False)
               )
def main(input_folder, output_folder):
    """segment all the files in the folder"""
    input_filenames = sorted(glob.glob(os.path.join(input_folder, "*.tif")))
    output_filename = os.path.join(
        output_folder,
        os.path.basename(input_filenames[0]))
    segmentation_command = "/sls/X02DA/data/e13657/Data20/quant-paper/Fiji.app/ImageJ-linux64 --ij2 --headless --run segment_macro.py 'input_file=\"{}\",output_file=\"{}\"'".format(
        input_filenames[0],
        output_filename
    )
    subprocess.check_call(segmentation_command, shell=True)
    output_filenames = glob.glob(
        os.path.join(output_folder, "*.tif"))
    for f in tqdm(output_filenames):
        compressed_filename = f.replace(
            ".tif",
            "_compressed.tif")
        command = "tiffcp -c packbits {} {}".format(
            f,
            compressed_filename)
        subprocess.check_call(command, shell=True)
        os.remove(f)


if __name__ == "__main__":
    main()
