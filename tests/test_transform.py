import unittest

import numpy as np

import raimad as rai

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

class TestCompo(unittest.TestCase):

    def test_transform(self):
        compo = BareStructural()
        geoms = compo.steamroll()

        # Test one root layer
        self.assertEqual(geoms.keys(), {'upper', 'lower'})

        # Test existence of polys
        self.assertEqual(len(geoms['upper']), 2)
        self.assertEqual(len(geoms['lower']), 2)

        # Test location
        self.assertEqual(list(geoms['upper'][0][2]), [20, 20])
        self.assertEqual(list(geoms['lower'][0][2]), [5, 5])

    def test_proxy_transform(self):
        compo = BareStructural()

        geoms_0 = compo.subcompos[0].steamroll()
        geoms_1 = compo.subcompos[1].steamroll()

        self.assertEqual(geoms_0.keys(), {'upper'})
        self.assertEqual(geoms_1.keys(), {'lower'})

        # Test existence of polys
        self.assertEqual(len(geoms_0['upper']), 2)
        self.assertEqual(len(geoms_1['lower']), 2)

        # Test location
        self.assertEqual(list(geoms_0['upper'][0][2]), [20, 20])
        self.assertEqual(list(geoms_1['lower'][0][2]), [5, 5])

    def test_walk_hier(self):
        mycompo = BareStructural()
        hier = list(mycompo.walk_hier())

        self.assertEqual(sum((compo is mycompo for compo in hier)), 1)
        self.assertEqual(
            sum(
                compo.final() is mycompo.subcompos[0].final()
                for compo in hier
                ),
            1)
        self.assertEqual(
            sum(
                compo.final() is mycompo.subcompos[1].final()
                for compo in hier
                ),
            1)

        self.assertEqual(sum((compo.depth() == 0 for compo in hier)), 1)
        self.assertEqual(sum((compo.depth() == 1 for compo in hier)), 2)


if __name__ == '__main__':
    unittest.main()

