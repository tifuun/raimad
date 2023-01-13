"""
I-Shaped Filter from DESHIMA2 project
"""

__author__ = "MaybE_Tree"
__credits__ = [
    "Kenichi Karatsu",
    ]

from PyClewinSDC.Component import Component, make_opts, make_layers
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.PolygonGroup import PolygonGroup
from PyClewinSDC.OptCategory import Geometric, Manufacture


class Filter(Component):
    optspecs = make_opts(
        Component,
        l_top=(
            70,
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

        meander_coup_spacing=(
            2,
            "Meander to coupler spacing",
            Geometric,
            ),

        line_coup_spacing=(
            2,
            "Line to coupler spacing (offset of line mark)",
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
            20,
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
            10,
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
        Ishape = self.make_Ishape()
        diel, gnd, optical = self.make_padding(Ishape)
        self.make_meander(diel, Ishape)

    def make_Ishape(self):
        """
        Generate the I-Shape on the electrobeam NbTiN layer
        """
        opts = self.opts

        beam = Polygon.rect_center(0, 0, opts.w_res, opts.l_res)
        top_coup = Polygon.rect_center(0, 0, opts.l_top, opts.w_coup)
        bot_coup = Polygon.rect_center(0, 0, opts.l_bot, opts.w_coup)

        top_coup.snap_top(beam)
        bot_coup.snap_bot(beam)

        Ishape = PolygonGroup(beam, top_coup, bot_coup)

        self.add_mark('line', Ishape.top_mid.move(0, opts.line_coup_spacing))

        self.add_subpolygons(Ishape, 'eb')
        return Ishape

    def make_padding(self, Ishape):
        """
        Generate Ground, optical NbTiN, and Dielectric layers.
        This function is for demonstration, I do not know
        the correct proprtions of the rectangles in these layers.
        """
        opts = self.opts

        diel = Polygon.rect_float(
            Ishape.bbox.width + 2 * opts.diel_pad,
            Ishape.bbox.height + 2 * opts.diel_pad,
            ).mid.align(Ishape.mid)

        optical = Polygon.rect_float(
            diel.bbox.width + 2 * opts.opt_pad,
            diel.bbox.height + 2 * opts.opt_pad,
            ).mid.align(Ishape.mid)

        gnd = Polygon.rect_float(
            optical.bbox.width + 2 * opts.gnd_pad,
            optical.bbox.height + 2 * opts.gnd_pad,
            ).mid.align(Ishape.mid)

        self.add_subpolygon(diel, 'diel')

        self.add_subpolygon(optical, 'opt')
        self.add_subpolygon(gnd, 'gnd')

        #padding_rects = PolygonGroup(diel, optical, gnd)

        return diel, gnd, optical

    def make_meander(self, diel, IShape):
        """
        Construct meander.
        """
        opts = self.opts

        # top part of meander, coupled to the filter
        horiz = Polygon.rect_float(opts.l_meander, opts.w_meander)

        base_side_meander_length = \
            opts.diel_pad - opts.meander_coup_spacing - opts.w_meander / 2

        # left part of meander, shorted to ground
        left = Polygon.rect_float(
            opts.w_meander,
            base_side_meander_length + opts.short_length,
            )

        # right part of meander, connected to mkid
        right = Polygon.rect_float(
            opts.w_meander,
            base_side_meander_length,
            )

        # Align the rectangles together into one wire
        left.top_mid.align(horiz.mid_left)
        right.top_mid.align(horiz.mid_right)

        # Fill in the corners with triangles to make a smooth wire

        tri = Polygon([[0, 0], [1, 1], [1, 0]])
        tri.scale(opts.w_meander / 2)

        tri_left = tri.copy()
        tri_right = tri.copy().vflip()

        tri_left.bot_right.align(horiz.mid_left)
        tri_right.bot_right.align(horiz.mid_right)

        meander = PolygonGroup(horiz, right, left, tri_left, tri_right)
        meander.top_mid.align(IShape.bot_mid)
        meander.movey(- opts.meander_coup_spacing)

        self.add_subpolygons(meander, 'eb')





