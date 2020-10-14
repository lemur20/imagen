""" Patterns combine a pattern function with a palette, and render at the given size (half the pattern period) with
    the given grayscale or color pixel type.
"""

from math import copysign
from random import choice
from pixfix import fixpix

__all__ = ['patterns', 'fetch_pattern']

def checker(size, palette):
    """A checkerboard pattern."""
    period = 2.0 * size
    return lambda x, y: palette[(x % period <= size) ^ (y % period <= size)]

def random_block(size, palette):
    """A random block pattern."""
    pixdict = {}
    ordinate = lambda x: int(x/size + copysign(1, x))
    def block(x, y):
        pixkey = (ordinate(x), ordinate(y))
        if pixkey not in pixdict:
            pixdict[pixkey] = choice(palette)
        return pixdict[pixkey]
    return block

def random_checker(size, palette):
    """A checkerboard pattern of random blocks."""
    ordinate = lambda x: int(x/size + copysign(1, x))
    pixel, pal = palette[0], palette[1:]
    period = 2.0 * size
    pixdict = {}
    def rand_check(x, y):
        if (x % period <= size) ^ (y % period <= size):
            pix = pixel
        else:
            pixkey = (ordinate(x), ordinate(y))
            if pixkey not in pixdict:
                pixdict[pixkey] = choice(pal)
            pix = pixdict[pixkey]
        return pix
    return rand_check

palettes = { # pixel values must be (8 bit) rgba so they can be down-channeled to gs, gsa, rgb
        'blackwhite': [b'\x00\x00\x00\xff', b'\xff\xff\xff\xff'],
        'bgbwg': [b'\x00\x00\x00\xff', b'\x00\x80\x00\xff', b'\x29\x29\xa3\xff', b'\xff\xff\xff\xff',
            b'\x50\x50\x50\xff'],
        'wgbbg': [b'\xff\xff\xff\xff', b'\x00\x80\x00\xff', b'\x29\x29\xa3\xff', b'\x00\x00\x00\xff',
            b'\x50\x50\x50\xff']
}

patterns = { # a pattern associates a pattern function with a palette
    'checker': [checker, 'blackwhite'],
    'block': [random_block, 'bgbwg'],
    'randcheck': [random_checker, 'wgbbg']
}


def fetch_pattern(pattern, pixtype, size):
    """Fetches a named pattern, sizes it, and down-channels the palette to the pixel type."""
    fxpx = fixpix(pixtype)
    palette = [fxpx(pixel) for pixel in palettes[patterns[pattern][1]]]
    pixfun = patterns[pattern][0](size, palette)
    return (pixfun, pixtype)

if __name__ == "__main__":
    from image import render, write
    from units import mm
    pixtype = 'rgb'
    for name in patterns.keys():
        scene = fetch_pattern(name, pixtype, 15*mm)
        img = render(scene)
        filename = "patterns_{0}.png".format(name)
        print("writing {0}".format(filename))
        write(filename, img)
