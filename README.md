# imagen
Imagen (Image Generation) is a png image generator written in python

Usage examples:

$ alias im="./imagen.py -v"
$ im pat checker 15mm test.png

Outputs a 15 millimeter black and white checkerboard pattern (default dimensions, resolution and pixel) to test.png

$ im -p a4 -r printer pat -x gs checker 15mm test.png

Same thing but with a page size of A4 and configured printer resolution. The pixels will be grayscale (gs)

$ im -s .25 pic -t dice.png test.png

Inputs dice.png to use as an image tile, outputs the tiling with tiles scaled by .25

Imagen provides a command line that can be customized to add in image transformations, convolutions, new patterns, etc.
The code is python 2.7.x & 3.x compatible and includes the png.py module courtesy of the pyPNG project.

