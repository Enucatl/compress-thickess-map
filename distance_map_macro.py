#@File(label="first file of the input sequence with the reconstructed 16 bit data") input_file
#@File(label="first file of the output sequence with the segmented data") output_file

from ij import IJ

print "opening", input_file 
IJ.run("Image Sequence...", "open=%s sort" %input_file)
print "geometry to distance map" 
IJ.run("Geometry to Distance Map", "threshold=128")
# print "distance map to distance ridge" 
# IJ.run("Distance Map to Distance Ridge")
print "save to", output_file 
IJ.saveAs("Raw Data", "%s" %output_file)
IJ.run("Quit")
