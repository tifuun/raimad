import unittest

import raimad as rai
import rai_faulty

class TestMyCompo(unittest.TestCase):
    def test_my_compo(self):
        compo = rai_faulty.MyCompo(width=12)
        self.assertEqual(compo.bbox.width, 12)

