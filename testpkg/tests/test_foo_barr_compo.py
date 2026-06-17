import unittest

import raimad as rai
import rai_testpkg

class TestFooBarrCompo(unittest.TestCase):
    def test_foo_barr_compo(self):
        compo = rai_testpkg.FooBarrCompo(width=12)
        self.assertEqual(compo.bbox.width, 12)

