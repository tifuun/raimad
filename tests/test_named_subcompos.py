import unittest

import pycif as pc

from .utils import ArrayAlmostEqual

class Compo_direct(pc.Compo):
    def _make(self):
        self.subcompos.beam = pc.RectWH(2, 20)
        self.subcompos.coup_top = pc.RectWH(10, 2)
        self.subcompos.coup_bot = pc.RectWH(8, 2)

        self.subcompos.beam.bbox.mid.to((0, 0))

        self.subcompos.coup_top.snap_above(self.subcompos.beam)
        self.subcompos.coup_bot.snap_below(self.subcompos.beam)

class Compo_auto(pc.Compo):
    def _make(self):
        beam = pc.RectWH(2, 20) @ 'root'
        coup_top = pc.RectWH(10, 2) @ 'root'
        coup_bot = pc.RectWH(8, 2) @ 'root'

        beam.bbox.mid.to((0, 0))

        coup_top.snap_above(beam)
        coup_bot.snap_below(beam)

        self.auto_subcompos()

#class Compo_shorthand(pc.Compo):
#    def _make(self):
#        beam = self.subcompo(pc.RectWH(2, 20), 'beam')
#        coup_top = self.subcompo(pc.RectWH(10, 2), 'coup_top')
#        coup_bot = self.subcompo(pc.RectWH(8, 2), 'coup_bot')
#
#        beam.bbox.mid.to((0, 0))
#
#        coup_top.snap_above(beam)
#        coup_bot.snap_below(beam)


class TestNamedSubcompos(ArrayAlmostEqual, unittest.TestCase, decimal=3):

    def test_named_subcompos(self):

        compo = Compo_direct()

        self.assertArrayAlmostEqual(
            compo.subcompos.coup_top.bbox.top_mid,
            (0, 20 / 2 + 2)
            )

        self.assertEqual(
            len(compo.subcompos),
            3
            )

    def test_named_subcompos_auto(self):

        compo = Compo_auto()

        self.assertArrayAlmostEqual(
            compo.subcompos.coup_top.bbox.top_mid,
            (0, 20 / 2 + 2)
            )

        self.assertEqual(
            len(compo.subcompos),
            3
            )

    #def test_named_subcompos_shorthand(self):

    #    compo = Compo_shorthand()

    #    self.assertArrayAlmostEqual(
    #        compo.subcompos.coup_top.bbox.top_mid,
    #        (0, 20 / 2 + 2)
    #        )

    #    self.assertEqual(
    #        len(compo.subcompos),
    #        3
    #        )


if __name__ == '__main__':
    unittest.main()

