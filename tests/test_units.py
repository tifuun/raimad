import unittest

import raimad as rai
import cift as cf

class TestUnits(unittest.TestCase):
    """
    Ensure handling of measurement units in RAIMAD/CIF
    """
    def test_micron(self):
        """
        Test that default raimad unit is micron (100 CIF units).
        """
        class Box(rai.Compo):
            def _make(self):
                self.geoms.update({'root': [[(0, 0), (1, 1), (1, 0)]]})

        exporter = rai.cif.noreuse(Box())
        cifstring = exporter.cif_string
        #print(cifstring)
        layers = cf.parse(cifstring)

        self.assertTrue(len(layers['ROOT'][0]) == 3)
        for x, y in layers['ROOT'][0]:
            self.assertIn(x, {0, 100})
            self.assertIn(y, {0, 100})

    def test_custom_multiplier(self):
        """
        Test passing custom multiplier to exporter
        """
        class Box(rai.Compo):
            def _make(self):
                self.geoms.update({'root': [[(0, 0), (1, 1), (1, 0)]]})

        exporter = rai.cif.noreuse(Box(), multiplier=420)
        cifstring = exporter.cif_string
        layers = cf.parse(cifstring)

        self.assertTrue(len(layers['ROOT'][0]) == 3)
        for x, y in layers['ROOT'][0]:
            self.assertIn(x, {0, 420})
            self.assertIn(y, {0, 420})



