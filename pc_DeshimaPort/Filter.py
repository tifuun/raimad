"""
I-Shaped Filter from DESHIMA2 project
"""

__author__ = "MaybE_Tree"
__credits__ = [
    "Kenichi Karatsu",
    ]

from PyClewinSDC.Component import Component, make_opts, make_layers
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.OptCategory import Geometric, Manufacture


class Filter(Component):
    optspecs = make_opts(
        Component,
        l_top=(
            100,
            "Top coupler length, edge to edge.",
            Geometric,
            ),

        w_coup=(
            0.8,
            "Coupler thickness (for both couplers)",
            Geometric,
            ),

        l_bot=(
            100,
            "Bottom coupler length, edge to edge.",
            Geometric,
            ),

        l_meander=(
            100,
            "Meander length. "
            "The meander is measured from the MIDDLE of the coupler "
            "to the opposite edge of the meander.",
            Geometric,
            ),

        w_meander=(
            1.5,
            "Meander width. Depends on MKID width",
            Geometric,
            ),

        l_res=(
            100,
            "Resonator length. "
            "Measured between inner edges of the two couplers, "
            "so a value of zero would result in two couplers sitting "
            "edge-to-edge to each other.",
            Geometric,
            ),

        w_res=(
            2,
            "Resonator width.",
            Geometric,
            ),

        diel_pad=(
            100,
            "Additional size to dielectric layer. "
            "At `diel_pad`=0, the dielectric layer barely fits the I-shape. ",
            Geometric
            ),

        opt_pad=(
            2,
            "Padding of optically exposed NbTiN layer to dielectric layer.",
            Manufacture,
            ),

        gnd_pad=(
            4,
            "Padding of NbTiN layer to optically exposed layer.",
            Manufacture,
            ),

        short_length=(
            100,
            "Length of the electrical short between coupler and ground layer.",
            Geometric
            ),

        )

    layerspecs = make_layers(
        Component,
        gnd=("NbTiN Ground", ),
        opt=("Optically exposed NbTiN", ),
        diel=("Dielectric", ),
        eb=("Electrobeam-deposited NbTiN", ),
        )

    def make(self):
        self.make_Ishape()
        self.make_padding()

    def make_Ishape(self):
        """
        Generate the I-Shape on the electrobeam NbTiN layer
        """
        opts = self.opts

        beam = Polygon.rect_center(0, 0, opts.w_res, opts.l_res)
        top_coup = Polygon.rect_center(0, 0, opts.l_top, opts.w_coup)
        bot_coup = Polygon.rect_center(0, 0, opts.l_bot, opts.w_coup)

        top_coup.snap_top(beam)
        bot_coup.snap_bottom(beam)

        self.add_subpolygons([beam, top_coup, bot_coup], 'eb')

    def make_padding(self):
        """
        Generate Ground, optical NbTiN, and Dielectric layers.
        This function is for demonstration, I do not know
        the correct proprtions of the rectangles in these layers.
        """


