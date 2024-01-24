import unittest

import pycif as pc

log = pc.get_logger(__name__)

class RectCompo(pc.Compo):
    class Layers(pc.Compo.Layers):
        root = pc.Layer()

    def _make(self):
        rect1 = pc.RectWH(10, 10).bbox.bot_left.to((0, 0))
        rect2 = rect1.copy().bbox.bot_left.rotate(pc.quartercircle / 10)
        rect3 = rect1.copy().bbox.bot_left.rotate(pc.quartercircle / 2)
        rect4 = pc.RectWH(10.5, 10.5).bbox.bot_left.to((.5, .5))

        self.add_subpoly(rect1)
        self.add_subpoly(rect2)
        self.add_subpoly(rect3)
        self.add_subpoly(rect4)

#class TestCoordinates(unittest.TestCase):
#    def test_coordinates(self):
#        compo = RectCompo()
#
#        with open('./test.cif', 'w') as f:
#            pc.export_cif(f, compo)

