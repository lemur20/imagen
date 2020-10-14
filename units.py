""" Converting between distances and pixel offsets or dimensions is easy to do provided that all distances
    and resolutions are in meters and pixels/meter respectively.

    For example, a letter-sized page with 1 inch margins has a image width of 6.5 inches. How many pixel
    columns is that on a 150 pixel/cm device?

    ncols = 6.5 inch X .0254 m/inch X 100 cm/m X 150 pixel/cm
          = (6.5 * units.inch) * (150 / units.cm)

    Just multiply by a unit for a meter distance, or divide for a meter resolution.
"""
import re

m = 1.0
cm = .01
mm = .001
inch = .0254 # 'in' is a keyword
ft = .3048

units = {'m': m, 'cm': cm, 'mm': mm, 'in': inch, 'ft': ft}

def distance(dl):
    """Inputs distance literal (e.g., 1.25cm or 3ft) outputs distance in meters."""
    match = re.search(r"^(\d*\.?\d*)([a-z]+)$", dl) # just the needed subset of floating point syntax
    if (match):
        try:
            value = float(match.group(1))
        except ValueError:
            raise ValueError("invalid distance value {0}".format(match.group(1)))
        try:
            unit = units[match.group(2)]
        except KeyError:
            raise ValueError("unrecognized distance unit {0}".format(match.group(2)))
    else:
        raise ValueError("unrecognized distance literal {0}".format(dl))
    return value*unit
