import unittest

import numpy as np

import pycif as pc

from .utils import ArrayAlmostEqual

class BareGeometric(pc.Compo):
    def _make(self):
        self.geoms.update({
            'root': [
                np.array([
                    [0, 0],
                    [0, 10],
                    [10, 10],
                    [10, 0],
                    ]),
                np.array([
                    [20, 20],
                    [40, 20],
                    [30, 40],
                    ]),
                ]
            })
        self.set_mark('triangle_corner', (20, 40))

class Intermid(pc.Compo):
    def _make(self):
        self.subcompos.append(
            pc.Proxy(
                BareGeometric(),
                {'root': 'intermediary'},
                pc.Transform().movex(-3)
                )
            )
        self.set_mark(
            'propagated',
            self.subcompos[0].get_mark('triangle_corner')
            )

class BareStructural(pc.Compo):
    def _make(self):
        self.subcompos.append(
            pc.Proxy(
                BareGeometric(),
                {'root': 'upper'},
                pc.Transform().scale(2)
                )
            )
        self.subcompos.append(
            pc.Proxy(
                BareGeometric(),
                {'root': 'lower'},
                pc.Transform().scale(0.5)
                )
            )
        self.subcompos.append(
            pc.Proxy(
                Intermid(),
                {'intermediary': 'lower'},
                pc.Transform().movey(-3)
                )
            )

        self.set_mark(
            'propagated',
            self.subcompos[2].get_mark('propagated')
            )

class BareGeometricSyntax(pc.Compo):
    def _make(self):
        self.geoms.update({
            'root': [
                np.array([
                    [0, 0],
                    [0, 10],
                    [10, 10],
                    [10, 0],
                    ]),
                np.array([
                    [20, 20],
                    [40, 20],
                    [30, 40],
                    ]),
                ]
            })
        self.marks.triangle_corner = (20, 40)

class IntermidSyntax(pc.Compo):
    def _make(self):
        self.subcompos.append(
            pc.Proxy(
                BareGeometricSyntax(),
                {'root': 'intermediary'},
                pc.Transform().movex(-3)
                )
            )
        self.set_mark(
            'propagated',
            self.subcompos[0].marks.triangle_corner
            )

class BareStructuralSyntax(pc.Compo):
    def _make(self):
        self.subcompos.append(
            pc.Proxy(
                BareGeometricSyntax(),
                {'root': 'upper'},
                pc.Transform().scale(2)
                )
            )
        self.subcompos.append(
            pc.Proxy(
                BareGeometricSyntax(),
                {'root': 'lower'},
                pc.Transform().scale(0.5)
                )
            )
        self.subcompos.append(
            pc.Proxy(
                IntermidSyntax(),
                {'intermediary': 'lower'},
                pc.Transform().movey(-3)
                )
            )

        self.marks.propagated = self.subcompos[2].marks.propagated

class TestMarks(ArrayAlmostEqual, unittest.TestCase, decimal=3):

    def test_marks(self):
        compo = BareStructural()

        self.assertArrayAlmostEqual(
            compo.get_mark('propagated'),
            (20 - 3, 40 - 3)
            )

        self.assertArrayAlmostEqual(
            compo.subcompos[2].subcompos[0].get_mark('triangle_corner'),
            (20 - 3, 40 - 3)
            )

        self.assertArrayAlmostEqual(
            compo.subcompos[2].get_mark('propagated'),
            (20 - 3, 40 - 3)
            )

    def test_marks_syntax(self):
        compo = BareStructuralSyntax()

        self.assertArrayAlmostEqual(
            compo.marks.propagated,
            (20 - 3, 40 - 3)
            )

        self.assertArrayAlmostEqual(
            compo.subcompos[2].subcompos[0].marks.triangle_corner,
            (20 - 3, 40 - 3)
            )

        self.assertArrayAlmostEqual(
            compo.subcompos[2].marks.propagated,
            (20 - 3, 40 - 3)
            )


if __name__ == '__main__':
    unittest.main()

