""" Pattern palettes and image mattes are defined by RGBA pixels and down-channeled to RGB or grayscale when needed. The
    module assumes 8-bit channels.
"""
import struct

__all__ = ['fixpix']

def to_gs(rgba):
    int_list = struct.unpack('<BBBB', rgba)
    average = int(round(sum(int_list[:3])/3.0))
    return struct.pack('<B', average)

def to_gsa(rgba):
    int_list = struct.unpack('<BBBB', rgba)
    average = int(round(sum(int_list[:3])/3.0))
    return struct.pack('<BB', average, int_list[3])

def to_rgb(rgba):
    return rgba[:3]

def to_rgba(rgba):
    return rgba

pixfix = {'gs': to_gs, 'gsa': to_gsa, 'rgb': to_rgb, 'rgba': to_rgba}

def fixpix(pixtype):
    """ Returns the pixel fixer for the specified pixel type."""
    return pixfix[pixtype]
