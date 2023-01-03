import numpy as np

from PyClewinSDC.Component import Component, make_opts, Shadow, make_layers
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.Dotdict import Dotdict
from PyClewinSDC.Transformable import Transformable as T


class LeakyDESHIMA(Component):
    """
    Leaky antenna for DESHIMA
    Long description Long description Long description
    Long description Long description Long description
    Long description Long description Long description
    Long description Long description Long description
    Long description Long description Long description
    Long description Long description Long description.
    """
    optspecs = make_opts(
        Component,
        width=(100, "Membrane width"),
        overlap=(2, "??? in um"),
        thickness=(100, "Membrane thickness"),
        )

    layerspecs = make_layers(
        Component,
        ('koh', ''),
        ('sin', ''),
        ('gns', 'Ground'),
        ('eb', 'Main Layer'),
        ('mesh', 'Mesh Layer'),
        ('diel', 'Dielectric'),
        )

    def make(self, opts=None):
        if opts is None:
            opts = self.opts

        self.make_butterfly(opts)

    def make_butterfly(self, opts):

        theta = np.radians(15)  # ??
        ladd0 = opts.overlap / np.tan((np.pi / 2 + theta) / 2)
        ladd1 = opts.overlap / np.tan((np.pi / 2 - theta) / 2)
        htotal = 351
        wtotal = 500
        wslot = 10  # ?? thickness of cpw?
        hslot = htotal * (wslot / 2) / (wtotal / 2)
        ltaper = (wtotal - wslot) / 2
        lcpwadd = 20

        #go(self.hSlot/2., self.wSlot/2.*updown)

        diagonal = Polygon(
            [
                [
                    0,
                    0,
                ],
                [
                    0,
                    2 * opts.overlap + ladd0,
                ],
                [
                    ltaper,
                    (htotal - hslot) / 2 + 2 * opts.overlap + ladd0,
                ],
                [
                    ltaper,
                    (htotal - hslot) / 2,
                ],
            ])

        self.add_subpolygon(
            diagonal.copy().movex(wslot/2),
            'eb',
            )

        self.add_subpolygon(
            diagonal.copy().hflip().movex(-wslot / 2),
            'eb',
            )
        
        self.add_subpolygon(
            diagonal.copy().hflip().vflip().move(-wslot / 2, -hslot / 2),
            'eb',
            )
        self.add_subpolygon(
            diagonal.copy().vflip().move(wslot/2, -hslot / 2),
            'eb',
            )

        barlength = htotal + 2 * opts.overlap + 2 * ladd1
        vertical = Polygon.rect_wh(
            0,
            -barlength / 2,
            2 * opts.overlap,
            barlength,
            )

        self.add_subpolygon(
            vertical.copy().movex(ltaper + 2 * opts.overlap),
            'eb',
            )

        self.add_subpolygon(
            vertical.copy().hflip().movex(-(ltaper + 2 * opts.overlap)),
            'eb',
            )

        #go(-self.hSlot/2., self.wSlot/2.*updown)


