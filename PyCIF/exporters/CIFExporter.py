"""
Caltech Intermediate Form Exporter
"""

import numpy as np

from PyCIF.Component import Component


def CIFExporter(stream, component: Component):
    stream.write('(CIF written by CleWin 3.1);\n')
    stream.write('(1 unit = 0.001 micron);\n')
    stream.write('(SRON);\n')
    stream.write('(Sorbonnelaan 2);\n')
    stream.write('(3584 CA  Utrecht);\n')
    stream.write('(Nederland);\n')

    for layer_name, polys in component.get_polygons().items():
        stream.write(f"L L{component.layerspecs[layer_name].index};\n")
        for poly in polys:
            stream.write('P ')
            for point in np.nditer(poly.get_xyarray()):
                point2 = point * 10  # TODO wtf??
                stream.write(f"{point2:9.0f} ")
            stream.write(';\n')

    stream.write('E\n')

