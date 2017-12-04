#@File(label="first file of the input sequence with the reconstructed 16 bit data") input_file
#@File(label="first file of the output sequence with the segmented data") output_file

from __future__ import division, print_function
from ij import IJ


print("opening %s" %input_file)
IJ.run("Image Sequence...", "open=%s sort" %input_file)
print("threshold with triangle method")
IJ.run("Make Binary", "method=Triangle background=Dark calculate")
print("erode")
IJ.run("Erode", "stack")
print("dilate")
IJ.run("Dilate", "stack")
print("save to %s" %output_file)
IJ.run("Image Sequence... ", "format=TIFF name=rec_16bit_segmented save=%s" %output_file)
