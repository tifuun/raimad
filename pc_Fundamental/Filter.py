import shapely as shp

from PyClewinSDC.Component import Component


class MSFilter(Component):
    """
    I-Shaped filter
    TODO explain what 'MS' stands for,
    I took this from the original codebase.
    """
    def __init__(self):
        super().__init__()

        self.add_layer('diel1', 'Dielectric 1')
        self.add_layer('diel2', 'Dielectric 2')
        self.add_layer('line', 'Through-line')
        self.add_layer('gnd', 'Ground')
        self.add_layer('eb', 'No clue lol')



