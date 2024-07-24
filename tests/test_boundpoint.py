"""
Autotests for boundpoint.
A boundpoint is a point tied to a proxy.
They can be used for performing transformations
relative to a specific point of a compo.
They are used in marks and bboxes.
For example, `mycompo.bbox.mid.to(0, 0)`
moves `mycompo` so that its middle (center of bounding box) is at the orign.
`mycompo.marks.coupler.hflip()` flips `mycompo` horizontally
around the mark called `coupler`.
"""

import unittest

import raimad as rai

from .utils import ArrayAlmostEqual

class BareGeometric(rai.Compo):
    def _make(self):
        self.geoms.update({
            'root': [
                [
                    [0, 0],
                    [40, 0],
                    [0, 40],
                    ],
                ]
            })
        # These are the two different syntaxes for assigning marks,
        # we want to test them both
        self.marks.corner_a = (0, 0)
        self.marks['corner_b'] = (0, 40)

class BareStructural(rai.Compo):
    def _make(self):
        self.subcompos.geometric = BareGeometric().proxy().move(3, 2)
        self.marks.corner_a = self.subcompos.geometric.marks.corner_a

class TestBoundpoint(ArrayAlmostEqual, unittest.TestCase):

    def test_boundpoint_mark(self):
        """
        Test that getting the mark on a compo gives
        the correct point
        """
        compo = BareGeometric()

        self.assertArrayAlmostEqual(
            compo.marks.corner_a,
            (0, 0)
            )

    def test_boundpoint_mark_translated(self):
        """
        Test that getting the mark on a proxy
        gives the correct point in external coordinates
        by applying the transform
        """
        compo = BareGeometric().proxy()
        compo.move(2, 3)

        self.assertArrayAlmostEqual(
            compo.marks["corner_a"],
            (2, 3)
            )

    def test_boundpoint_mark_subcompo(self):
        """
        Test that getting the mark from a subcompo
        still computes the external coordinates correctly
        """
        compo = BareStructural()

        self.assertArrayAlmostEqual(
            compo.subcompos.geometric.marks.corner_a,
            (3, 2)
            )

    def test_boundpoint_mark_subcompo_translated(self):
        """
        Test that getting the mark from a subcompo of a proxy
        still computes the external coordinates correctly
        (i.e. applies the transform done inside the structural
        componenet, and the transform done by the proxy created this function)
        """
        compo = BareStructural().proxy()
        compo.move(10, 20)

        self.assertArrayAlmostEqual(
            compo.subcompos.geometric.marks.corner_a,
            (3 + 10, 2 + 20)
            )

    def test_boundpoint_bbox_subcompo_translated(self):
        compo = BareStructural().proxy()
        compo.move(10, 20)

        self.assertArrayAlmostEqual(
            compo.subcompos.geometric.bbox.bot_left,
            (3 + 10, 2 + 20)
            )

if __name__ == '__main__':
    unittest.main()

