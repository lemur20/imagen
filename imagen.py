#!/usr/bin/env python
"""Imagen (Image Generation) renders a png image as specified by the command line."""

import argparse
import image
import units
import pages
import patterns

__all__ = ['cmd_parser', 'generate_scene', 'render_scene', 'view_scene']

def distance_type(d):
    try:
        return units.distance(d)
    except ValueError as e:
        raise argparse.ArgumentTypeError(e)

def cmd_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-v", "--verbose", action='store_true', help="verbosity")
    parser.add_argument("-p", "--page", choices=pages.pages.keys(),
        default=pages.default_page, help="page dimensions")
    parser.add_argument("-r", "--resolution", choices=pages.resolutions.keys(),
        default=pages.default_resolution, help="page resolution")
    parser.add_argument("-s", "--scale", default=1.0, type=float, help="object scaling")

    subparsers = parser.add_subparsers(help="sub-command help", dest="picpat")
    pic_parser = subparsers.add_parser("pic", help="renders the picture supplied as a PNG file")
    picopts = pic_parser.add_mutually_exclusive_group()
    picopts.add_argument("-t", "--tile", action="store_true", help="tile the image")
    picopts.add_argument("-m", "--matte", choices=image.mattes.keys(),
        default=image.default_matte, help="background matte for centered picture")
    pic_parser.add_argument("infile", type=argparse.FileType('rb'), help="input png file")

    pat_parser = subparsers.add_parser("pat", help="renders a pattern")
    pat_parser.add_argument("-x", "--pixtype", default='rgb',
        choices=['gs', 'gsa', 'rgb', 'rgba'],
        help="pixel types include grayscale and rgb with or without alpha channel")
    pat_parser.add_argument("pattern", choices=patterns.patterns.keys(), help="a configured pattern")
    pat_parser.add_argument("pattern_size", type=distance_type, help="size of pattern, e.g., 15mm or .25in")

    parser.add_argument("outfile", type=argparse.FileType('wb'), help="output png file")

    return parser

def generate_scene(args):
    """Returns a pixel function for the specified scene."""
    if args.picpat == "pic":
        img = image.read(args.infile).scale(args.scale)
        if (args.tile):
            scene = image.tile(img)
        else:
            scene = image.center(img, image.mattes[args.matte])
    else: # "pat" subcommand
        size = args.pattern_size * args.scale
        scene = patterns.fetch_pattern(args.pattern, args.pixtype, size)
    return scene

def render_scene(args, scene):
    """Renders the scene to an image using defined page and resolution."""
    page = pages.pages[args.page]
    resolution = pages.resolutions[args.resolution]
    img = image.render(scene, page, resolution)
    return img

def view_scene(scene, xform):
    """Applies a transformation to the scene."""
    pixfun, pixtype = scene[0], scene[1]
    return lambda x, y: pixfun(*xform(x, y)), pixtype

def timestr(s):
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(round(seconds)))

if __name__ == "__main__":
    import time, sys
    parser = cmd_parser()
    args = parser.parse_args()
    t1 = time.time()
    scene = generate_scene(args)
    view = view_scene(scene, lambda x, y: (x,y)) # identity transformation as example
    img = render_scene(args, view)
    image.write(args.outfile, img)
    t2 = time.time()
    if args.verbose:
        sys.stderr.write("{0} {1}x{2} {3}\n".format(args.outfile.name, img.cols, img.rows, timestr(t2-t1)))
