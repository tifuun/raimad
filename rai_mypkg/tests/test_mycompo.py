import unittest

import raimad as rai
import rai_mypkg

class Testmycompo(unittest.TestCase):
    def test_mycompo(self):
        compo = rai_mypkg.mycompo(width=12)
        self.assertEqual(compo.bbox.width, 12)

