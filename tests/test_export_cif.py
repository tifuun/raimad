import unittest
from io import StringIO

import pycif as pc

log = pc.get_logger(__name__)

class TestExportCif(unittest.TestCase):
    def test_export_cif(self):
        compo = pc.Snowman()

        io = StringIO()
        pc.export_cif(io, compo)
        cif = io.getvalue()

        num_polys = cif.count('P')
        self.assertEqual(num_polys, 6)


