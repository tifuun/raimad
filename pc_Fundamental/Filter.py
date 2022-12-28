from PyClewinSDC.Component import Component, make_opts, Shadow
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.Dotdict import Dotdict


#def MSFilter(direction, updown, ii, line_hybrid, w_coarse, w_upper, short_length, dummy_offset,
#             fpre, f0, eps_eff, filter_lengths,
#             diellayer1, gndlayer, diellayer2, linelayer, linelayerEB,
#             n_space=0, drawFilter=True, bPatch=False, bNarrowGap=False):

class MSFilter(Component):
    """
    I-Shaped filter
    This is a bandpass filter,
    it works as a resonator and only lets in a specific frequency.
    I don't really know what 'MS' stands for,
    this comes from the original PyClewin codebase.
    Anyway, this is just some filler to pad out the description.
    """
    optspecs = make_opts(
        Component,
        top_length=(100, "Length of the top part of the filter"),
        bottom_length=(70, "Length of the bottom part of the filter"),
        top_thickness=(10, "Thickness of the top part of the filter"),
        bottom_thickness=(10, "Thickness of the bottom part of the filter"),
        beam_length=(100, "Length of the beam"),
        beam_thickness=(10, "Thickness of the beam"),
        )

    def __init__(self):
        super().__init__()

        self.add_layer('diel1', 'Dielectric 1')
        self.add_layer('diel2', 'Dielectric 2')
        self.add_layer('line', 'Through-line')
        self.add_layer('gnd', 'Ground')
        self.add_layer('eb', 'No clue lol')

    def make(self, opts=None):
        if opts is None:
            opts = self.opts

        # bottom
        self.add_subpolygon(
            Polygon.rect_wh(
                - opts.bottom_length / 2,
                0,
                opts.bottom_length,
                opts.bottom_thickness,
                ),
            'eb',
            )

        # top
        self.add_subpolygon(
            Polygon.rect_wh(
                - opts.top_length / 2,
                opts.beam_length,
                opts.top_length,
                opts.top_thickness,
                ),
            'eb',
            )

        # beam
        self.add_subpolygon(
            Polygon.rect_wh(
                - opts.beam_thickness / 2,
                0,
                opts.beam_thickness / 2,
                opts.beam_length,
                ),
            'eb',
            )


class MSFilterParametric(MSFilter):
    """
    I-Shaped filter -- Parametric design
    But this one now takes function-based parameters
    like frequency in order to compute the geometric parameters
    , which is probably more useful
    """
    optspecs = make_opts(
        MSFilter,
        f0=(1e6, "Base frequency"),
        top_length=Shadow,
        )

