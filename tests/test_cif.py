import unittest
import re

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


# Regext to find procedure calls in CIF file
find_procedure_calls = re.compile(r"^\s*C (\w+);", re.MULTILINE)


class TestCIF(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.compo = BareStructural()
        self.cif_string = pc.export_cif(self.compo)

    def test_cif_polys(self):

        num_polys = self.cif_string.count('P')
        self.assertEqual(num_polys, 6)

        #num_layers = cif_string.count('L') / 2
        #self.assertEqual(num_layers, 2)
        # TODO extract layers and check unique

    def test_cif_transforms(self):
        # Check that the transforms worked
        self.assertTrue('80000 40000' in self.cif_string)
        self.assertTrue('20000 10000' in self.cif_string)

    def test_cif_subcompo(self):
        # polygon from compo included in Intermediary
        self.assertTrue(
            f'{(30 - 3) * 1000} {(40 - 3) * 1000}' in self.cif_string)

    def test_cif_procedure_numbers(self):
        """
        Test that procedure calls are not repeated.
        Also check that procedure numbers start at 1.
        This was a bug in an earlier version.
        """
        procedure_calls = find_procedure_calls.findall(self.cif_string)
        self.assertTrue(pc.iters.is_distinct(procedure_calls))
        self.assertEqual(sorted(map(int, procedure_calls))[0], 1)


if __name__ == '__main__':
    unittest.main()

