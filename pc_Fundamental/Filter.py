from PyClewinSDC.Component import Component
from PyClewinSDC.Dotdict import Dotdict


#def MSFilter(direction, updown, ii, line_hybrid, w_coarse, w_upper, short_length, dummy_offset,
#             fpre, f0, eps_eff, filter_lengths,
#             diellayer1, gndlayer, diellayer2, linelayer, linelayerEB,
#             n_space=0, drawFilter=True, bPatch=False, bNarrowGap=False):

class MSFilter(Component):
    """
    I-Shaped filter
    TODO explain what 'MS' stands for,
    I took this from the original codebase.
    """
    default_opts = Dotdict(
        Component.default_opts,
        )

    def __init__(self):
        super().__init__()

        self.add_layer('diel1', 'Dielectric 1')
        self.add_layer('diel2', 'Dielectric 2')
        self.add_layer('line', 'Through-line')
        self.add_layer('gnd', 'Ground')
        self.add_layer('eb', 'No clue lol')



