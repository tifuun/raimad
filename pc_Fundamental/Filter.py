from PyClewinSDC.Component import Component
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
    default_opts = Dotdict(
        Component.default_opts,
        top_length=100,
        bottom_length=70,
        top_thickness=10,
        bottom_thickness=10,
        beam_length=100,
        beam_thickness=10,
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


