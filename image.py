"""Reads, writes and renders PNG images. Provides "center" and "tile" to define image-based pixel functions. The module
   uses pyPNG to read and write the files. 
"""
import png
import pages
from pixfix import fixpix

__all__ = ['read', 'write', 'render', 'tile', 'center', 'matte']

default_page = pages.pages[pages.default_page]
default_resolution = pages.resolutions[pages.default_resolution]

class Image(object):
    """The subclasses of Image together with the read & write calls constitute the interface to the png module."""
    def __init__(self, rows, cols, resolution, pixtype):
        self.rows = rows
        self.cols = cols
        self.res = resolution
        self.pixtype = pixtype

class InputImage(Image):
    """An input image is read from a file/stream and provides random access to pixels."""
    def __init__(self, rows, cols, resolution, pixtype, pixels):
        Image.__init__(self, rows, cols, resolution, pixtype)
        self.pixels = pixels
    def scale(self, s):
        """"Returns an image scaled up by scaling resolution down."""
        return InputImage(self.rows, self.cols, self.res/s, self.pixtype, self.pixels)

class OutputImage(Image):
    """Python can't do multicore renders, so there's no reason to buffer more than one output pixel row."""
    def __init__(self, rows, cols, resolution, pixtype, rowgen):
        Image.__init__(self, rows, cols, resolution, pixtype)
        self.rowgen = rowgen

def read(f):
    """Reads PNG file."""

    if type(f) == str:
        f = open(f, 'rb')
    reader = png.Reader(file=f)
    cols, rows, pixgen, info  = reader.asDirect()

    if info['greyscale']:
        pixtype = 'gsa' if info['alpha'] else 'gs'
    else:
        pixtype = 'rgba' if info['alpha'] else 'rgb'

    try:
        x, y, meters = info['physical']
        if meters:
            resolution = x
        else:
            resolution = default_resolution
    except KeyError: # no pHYs chunk defined
        resolution = default_resolution

    # need pixels in memory for random access
    pixels = bytearray()
    for pixrow in pixgen:
        pixels.extend(pixrow)
    f.close()

    return InputImage(rows, cols, resolution, pixtype, pixels)

def write(f, img):
    """Writes PNG file."""
    if type(f) == str:
        f = open(f, 'wb')
    gray = img.pixtype == 'gs' or img.pixtype == 'gsa'
    alpha = img.pixtype == 'gsa' or img.pixtype == 'rgba'
    pixels_per_meter = int(round(img.res)) # imagen code uses same resolution units as png
    w = png.Writer(width=img.cols, height=img.rows, greyscale=gray, alpha=alpha,
        x_pixels_per_unit=pixels_per_meter, y_pixels_per_unit=pixels_per_meter, unit_is_meter=True)
    w.write(f, img.rowgen)
    f.close()
    return 0

channels = {'gs': 1, 'gsa': 2, 'rgb': 3, 'rgba': 4}

def render(pixpair, page=default_page, res=default_resolution):
    """Renders a pixel function to an image."""
    rows, cols  = int(round(res * page.image_height())), int(round(res * page.image_width()))
    pixfun, pixtype = pixpair[0], pixpair[1]
    pixsize = channels[pixtype] # assumes 8-bit channels
    hw, hh = page.image_width() / 2.0, page.image_height() / 2.0
    pixrow = bytearray(cols*pixsize)

    def row_generator():
        for r in range(rows):
            for c in range(cols):
                h, v  = c/res, r/res # horiz, vert offsets from top left
                x, y = h - hw, hh - v
                offset = c * pixsize
                pixrow[offset:offset+pixsize] = pixfun(x, y)
            yield pixrow
    return OutputImage(rows, cols, res, pixtype, row_generator())

# must be rgba and should be a clear color
mattes = {'white': b'\xff\xff\xff\x00', 'black': b'\x00\x00\x00\x00'}
default_matte = 'white'

def center(img, matte=mattes[default_matte]):
    """Returns a pixel function to render a centered image."""
    rows, cols, res = img.rows, img.cols, img.res
    pixels, pixsize = img.pixels, channels[img.pixtype] # assumes 8-bit channels
    width, height = cols/res, rows/res
    matte_pixel = fixpix(img.pixtype)(matte) # match the image pixel type

    def centered(x, y):
        h, v = x + width/2.0, height/2.0 - y # horz, vert offset from top left
        r, c = int(round(v*res)), int(round(h*res))
        if (r>=0 and r<rows and c>=0 and c<cols):
            offset = (cols*r + c)*pixsize
            return pixels[offset:offset+pixsize]
        else:
            return matte_pixel
    return (centered, img.pixtype)

def tile(img):
    """Returns a pixel function to render a tiled image."""
    rows, cols, res  = img.rows, img.cols, img.res
    pixels, pixsize = img.pixels, channels[img.pixtype] # assumes 8-bit channels
    width, height = cols/res, rows/res

    def tiled(x, y):
        h = (x + width/2.0) % width # horz, vert offset from top left
        v = (height/2.0 - y) % height 
        r, c = int(v*res), int(h*res)
        offset = (cols*r + c)*pixsize
        return pixels[offset:offset+pixsize]
    return (tiled, img.pixtype)

if __name__ == "__main__":

    def write_image(name, fn, src):
        img = render(fn(src))
        print("writing {}".format(name))
        write(name, img)

    src = read("dice.png")
    write_image("image_tile.png", tile, src.scale(0.25))
    write_image("image_center.png", center, src)

