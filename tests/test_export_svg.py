import unittest
from io import StringIO

import pycif as pc

log = pc.get_logger(__name__)

class TestExportSvg(unittest.TestCase):
    def test_export_svg(self):
        compo = pc.Snowman()

        io = StringIO()
        pc.export_svg(io, compo)
        cif = io.getvalue()

        num_polys = cif.count('<polygon')
        self.assertEqual(num_polys, 6)


