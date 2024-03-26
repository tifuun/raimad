import unittest

import numpy as np

import pycif as pc

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

class Intermid(pc.Compo):
    def _make(self):
        self.subcompos.append(
            pc.Proxy(
                BareGeometric(),
                {'root': 'intermediary'},
                pc.Transform().movex(-3)
                )
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

class TestCIF(unittest.TestCase):

    def test_cif(self):
        compo = BareStructural()
        cif_string = pc.export_cif(compo)

        #with open('/tmp/wtf.cif', 'w') as f: f.write(cif_string)

        num_polys = cif_string.count('P')
        self.assertEqual(num_polys, 6)

        #num_layers = cif_string.count('L') / 2
        #self.assertEqual(num_layers, 2)
        # TODO extract layers and check unique

        # Check that the transforms worked
        self.assertTrue('80000 40000' in cif_string)
        self.assertTrue('20000 10000' in cif_string)

        # polygon from compo included in Intermediary
        self.assertTrue(f'{(30 - 3) * 1000} {(40 - 3) * 1000}' in cif_string)


if __name__ == '__main__':
    unittest.main()

