"""Defines page dimensions and resolutions."""
from units import mm, inch

class Page:
    def __init__(self, width, height, hmargin=0, vmargin=0):
        self.width = width
        self.height = height
        self.hmargin = hmargin
        self.vmargin = vmargin

    def image_width(self):
        return self.width - 2.0*self.hmargin
    def image_height(self):
        return self.height - 2.0*self.vmargin
    def turn(self):
        return Page(self.height, self.width, self.vmargin, self.hmargin)

pages  = {
#    'screen': Page(250*mm, 250*mm),
    'screen': Page(280*mm, 280*mm),
    'letter': Page(8.5*inch, 11*inch, 1*inch, 1*inch),
        'a0': Page(841*mm, 1189*mm),
        'a4': Page(210*mm, 297*mm, 25*mm, 25*mm)
}
default_page = 'screen'

resolutions = {
        'screen': 81.59/inch,
        'printer': 300.0/inch
}
default_resolution = 'screen'

