"""
Caltech Intermediate Form Exporter.
"""

from io import IOBase, StringIO
from pathlib import Path

import numpy as np
import pycif as pc

def _export_cif(stream, compo: pc.Compo, multiply=1e3):
    """
    Export CIF file to stream.
    """
    stream.write('(CIF written by CleWin 3.1);\n')
    stream.write('(1 unit = 0.001 micron);\n')
    stream.write('(SRON);\n')
    stream.write('(Sorbonnelaan 2);\n')
    stream.write('(3584 CA  Utrecht);\n')
    stream.write('(Nederland);\n')

    subpolys = sorted(
        compo.get_subpolygons(),
        key=lambda subpoly: subpoly.layer
        )

    prev_layer = None
    for subpoly in subpolys:
        if subpoly.layer != prev_layer:
            stream.write(f'L L{subpoly.layer};\n')

        xyarray = subpoly.polygon.get_xyarray() * multiply

        if len(xyarray) == 0:
            continue

        stream.write('P ')

        try:
            for point in np.nditer(xyarray):
                point2 = point
                stream.write(f'{point2:9.0f} ')
            stream.write(';\n')

        except Exception as e:
            raise Exception(
                f'Failed to export polygon {subpoly}. ',
                ) from e

    stream.write('E\n')

def export_cif(
        compo: pc.Compo,
        dest: None | str | Path | IOBase = None):
    """
    Export CIF file as string or to stream or to filename
    """
    if dest is None:
        stream = StringIO()
        _export_cif(stream, compo)
        return stream.getvalue()

    elif isinstance(dest, str | Path):
        with open(dest, 'w') as file:
            _export_cif(file, compo)

    elif isinstance(dest, IOBase):
        _export_cif(dest, compo)

    else:
        raise Exception(f"Cannot export to {dest}")

