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
                )
            )
        self.subcompos.append(
            rai.Proxy(
                BareGeometric(),
                {'root': 'lower'},
                )
            )

class TestCompo(unittest.TestCase):

    def test_bare_geometric(self):
        compo = BareGeometric()
        geom = compo.steamroll()

        # Test one root layer
        self.assertEqual(geom.keys(), {'root'})

        # Test two polys on the layer
        self.assertEqual(len(geom['root']), 2)

    def test_bare_geometric_copied(self):
        compo = BareGeometric()
        self.assertIsNot(compo.geoms, compo.steamroll())

    def test_bare_structural(self):
        compo = BareStructural()
        geom = compo.steamroll()

        # Test one root layer
        self.assertEqual(geom.keys(), {'upper', 'lower'})

        # Test two polys on the top lyaer
        self.assertEqual(len(geom['upper']), 2)

        # Test two polys on the top lyaer
        self.assertEqual(len(geom['lower']), 2)


if __name__ == '__main__':
    unittest.main()

