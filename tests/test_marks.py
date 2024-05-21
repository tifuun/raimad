import unittest

import numpy as np

import raimad as rai

from .utils import ArrayAlmostEqual

class BareGeometric(rai.Compo):
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

class Intermid(rai.Compo):
    def _make(self):
        self.subcompos.append(
            rai.Proxy(
                BareGeometric(),
                {'root': 'intermediary'},
                rai.Transform().movex(-3)
                )
            )
        self.set_mark(
            'propagated',
            self.subcompos[0].get_mark('triangle_corner')
            )

class BareStructural(rai.Compo):
    def _make(self):
        self.subcompos.append(
            rai.Proxy(
                BareGeometric(),
                {'root': 'upper'},
                rai.Transform().scale(2)
                )
            )
        self.subcompos.append(
            rai.Proxy(
                BareGeometric(),
                {'root': 'lower'},
                rai.Transform().scale(0.5)
                )
            )
        self.subcompos.append(
            rai.Proxy(
                Intermid(),
                {'intermediary': 'lower'},
                rai.Transform().movey(-3)
                )
            )

        self.set_mark(
            'propagated',
            self.subcompos[2].get_mark('propagated')
            )

class BareGeometricSyntax(rai.Compo):
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

class IntermidSyntax(rai.Compo):
    def _make(self):
        self.subcompos.append(
            rai.Proxy(
                BareGeometricSyntax(),
                {'root': 'intermediary'},
                rai.Transform().movex(-3)
                )
            )
        self.set_mark(
            'propagated',
            self.subcompos[0].marks.triangle_corner
            )

class BareStructuralSyntax(rai.Compo):
    def _make(self):
        self.subcompos.append(
            rai.Proxy(
                BareGeometricSyntax(),
                {'root': 'upper'},
                rai.Transform().scale(2)
                )
            )
        self.subcompos.append(
            rai.Proxy(
                BareGeometricSyntax(),
                {'root': 'lower'},
                rai.Transform().scale(0.5)
                )
            )
        self.subcompos.append(
            rai.Proxy(
                IntermidSyntax(),
                {'intermediary': 'lower'},
                rai.Transform().movey(-3)
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

