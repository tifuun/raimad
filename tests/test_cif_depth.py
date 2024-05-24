import unittest

import raimad as rai

class TestCIFDepth(unittest.TestCase):

    def test_cif_dfs_rect(self):
        """
        """
        compo = rai.RectWH(10, 5)

        exporter = rai.cif.CIFDepth(
            compo,
            multiplier=1,
            )






if __name__ == '__main__':
    unittest.main()

