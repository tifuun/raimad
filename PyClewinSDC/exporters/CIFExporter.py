"""
Caltech Intermediate Form Exporter
"""

from io import StringIO

import numpy as np

from PyClewinSDC.exporters.Exporter import Exporter
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.LayerParams import LayerParams


class CIFExporter(Exporter):
    def __init__(self, output=None):
        self.output = output or StringIO()

    def writeline(self, text=''):
        self.output.write(''.join((text, '\n')))

    def write(self, text):
        self.output.write(text)

    def write_header(self):
        self.writeline('(CIF written by CleWin 3.1);')
        self.writeline('(1 unit = 0.001 micron);')
        self.writeline('(SRON);')
        self.writeline('(Sorbonnelaan 2);')
        self.writeline('(3584 CA  Utrecht);')
        self.writeline('(Nederland);')

    def write_footer(self):
        self.writeline('E')

    def write_polygon(self, polygon: Polygon):
        self.write('P ')
        for point in np.nditer(polygon.xyarray):
            self.write(f"{point:6.0f} ")
        self.writeline(';')

    def write_layer(self, layer: LayerParams):
        self.writeline(f"L L{layer.index};")

