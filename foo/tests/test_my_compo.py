import unittest

import raimad as rai
import rai_mypkg

class TestMyCompo(unittest.TestCase):
    def test_my_compo(self):
        compo = rai_mypkg.MyCompo(width=12)
        self.assertEqual(compo.bbox.width, 12)

